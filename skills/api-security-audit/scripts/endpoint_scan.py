#!/usr/bin/env python3
"""
Endpoint Scanner - Mapeia endpoints de uma API para análise de segurança.
Uso: python endpoint_scan.py --base-url https://api.example.com --token $TOKEN
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Erro: requests não instalado. Execute: pip install requests")
    sys.exit(1)


def scan_common_endpoints(base_url: str, token: Optional[str] = None) -> list[dict]:
    """Testa endpoints comuns em APIs REST."""
    
    common_paths = [
        # Auth
        "/api/auth/login",
        "/api/auth/register", 
        "/api/auth/logout",
        "/api/auth/refresh",
        "/api/auth/me",
        "/api/auth/forgot-password",
        # Users
        "/api/users",
        "/api/users/me",
        "/api/user",
        "/api/profile",
        # Admin
        "/api/admin",
        "/api/admin/users",
        "/api/admin/settings",
        "/api/admin/logs",
        # Common resources
        "/api/posts",
        "/api/products",
        "/api/orders",
        "/api/organizations",
        "/api/settings",
        # Health/Debug
        "/health",
        "/api/health",
        "/debug",
        "/api/debug",
        "/metrics",
        "/api/metrics",
        "/.env",
        "/api/swagger",
        "/api/docs",
        "/swagger.json",
        "/openapi.json",
    ]
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    results = []
    
    for path in common_paths:
        url = f"{base_url.rstrip('/')}{path}"
        try:
            # GET
            resp = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            if resp.status_code != 404:
                results.append({
                    "method": "GET",
                    "path": path,
                    "status": resp.status_code,
                    "size": len(resp.content),
                    "auth_required": resp.status_code == 401,
                })
            
            # POST (só em endpoints de auth/create)
            if any(x in path for x in ["login", "register", "create", "users"]):
                resp = requests.post(url, headers=headers, json={}, timeout=5)
                if resp.status_code not in [404, 405]:
                    results.append({
                        "method": "POST",
                        "path": path,
                        "status": resp.status_code,
                        "size": len(resp.content),
                    })
                    
        except requests.exceptions.RequestException as e:
            pass  # Silently skip connection errors
    
    return results


def analyze_openapi(base_url: str) -> list[dict]:
    """Tenta extrair endpoints do OpenAPI/Swagger."""
    
    openapi_paths = ["/openapi.json", "/swagger.json", "/api/docs/openapi.json"]
    
    for path in openapi_paths:
        try:
            resp = requests.get(f"{base_url.rstrip('/')}{path}", timeout=5)
            if resp.status_code == 200:
                spec = resp.json()
                endpoints = []
                
                for path, methods in spec.get("paths", {}).items():
                    for method, details in methods.items():
                        if method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                            endpoints.append({
                                "method": method.upper(),
                                "path": path,
                                "summary": details.get("summary", ""),
                                "auth": bool(details.get("security")),
                            })
                
                return endpoints
        except Exception:
            pass
    
    return []


def check_security_headers(base_url: str) -> dict:
    """Verifica headers de segurança."""
    
    security_headers = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
    ]
    
    try:
        resp = requests.get(base_url, timeout=5)
        present = []
        missing = []
        
        for header in security_headers:
            if header.lower() in [h.lower() for h in resp.headers]:
                present.append(header)
            else:
                missing.append(header)
        
        return {
            "present": present,
            "missing": missing,
            "cors": resp.headers.get("Access-Control-Allow-Origin", "Not set"),
        }
    except:
        return {"error": "Failed to connect"}


def main():
    parser = argparse.ArgumentParser(description="API Endpoint Scanner")
    parser.add_argument("--base-url", required=True, help="Base URL da API")
    parser.add_argument("--token", help="Bearer token para autenticação")
    parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")
    args = parser.parse_args()
    
    print(f"🔍 Scanning: {args.base_url}\n")
    
    # 1. Tentar OpenAPI
    print("📄 Buscando OpenAPI spec...")
    openapi_endpoints = analyze_openapi(args.base_url)
    if openapi_endpoints:
        print(f"   ✅ Encontrados {len(openapi_endpoints)} endpoints via OpenAPI\n")
    
    # 2. Scan manual
    print("🌐 Testando endpoints comuns...")
    scanned_endpoints = scan_common_endpoints(args.base_url, args.token)
    print(f"   ✅ Encontrados {len(scanned_endpoints)} endpoints ativos\n")
    
    # 3. Headers de segurança
    print("🔒 Verificando headers de segurança...")
    headers = check_security_headers(args.base_url)
    
    # Resultado
    result = {
        "target": args.base_url,
        "openapi_endpoints": openapi_endpoints,
        "discovered_endpoints": scanned_endpoints,
        "security_headers": headers,
    }
    
    # Output
    print("\n" + "="*60)
    print("📊 RESULTADO DO SCAN")
    print("="*60)
    
    print("\n🔗 Endpoints Descobertos:")
    for ep in scanned_endpoints:
        status_emoji = "✅" if ep["status"] < 400 else "🔒" if ep["status"] == 401 else "❌"
        print(f"   {status_emoji} {ep['method']:6} {ep['path']:40} [{ep['status']}]")
    
    print("\n🔒 Headers de Segurança:")
    if "error" not in headers:
        for h in headers.get("missing", []):
            print(f"   ⚠️  FALTANDO: {h}")
        print(f"   CORS: {headers.get('cors', 'N/A')}")
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Resultado salvo em: {args.output}")
    
    return result


if __name__ == "__main__":
    main()
