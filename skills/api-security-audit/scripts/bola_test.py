#!/usr/bin/env python3
"""
BOLA (Broken Object Level Authorization) Tester
Testa se endpoints permitem acesso a recursos de outros usuários.

Uso: python bola_test.py --url "https://api.example.com/users/{id}" \
                         --token-a $TOKEN_USER_A \
                         --token-b $TOKEN_USER_B \
                         --id-a $USER_A_ID \
                         --id-b $USER_B_ID
"""

import argparse
import json
import sys
from typing import Optional

try:
    import requests
except ImportError:
    print("Erro: requests não instalado. Execute: pip install requests")
    sys.exit(1)


def test_bola(
    url_template: str,
    token_a: str,
    token_b: str,
    id_a: str,
    id_b: str,
    methods: list[str] = ["GET"]
) -> list[dict]:
    """
    Testa BOLA tentando acessar recursos com tokens cruzados.
    
    Cenários:
    1. User A acessa recurso de User A (deve funcionar)
    2. User A acessa recurso de User B (deve falhar com 403)
    3. User B acessa recurso de User A (deve falhar com 403)
    """
    
    results = []
    
    test_cases = [
        {"name": "A acessa A (legítimo)", "token": token_a, "id": id_a, "should_succeed": True},
        {"name": "A acessa B (BOLA)", "token": token_a, "id": id_b, "should_succeed": False},
        {"name": "B acessa A (BOLA)", "token": token_b, "id": id_a, "should_succeed": False},
        {"name": "B acessa B (legítimo)", "token": token_b, "id": id_b, "should_succeed": True},
    ]
    
    for method in methods:
        # DELETE legítimo apaga o recurso; os acessos cruzados precisam vir antes
        cases = sorted(test_cases, key=lambda t: t["should_succeed"]) if method == "DELETE" else test_cases
        for test in cases:
            url = url_template.replace("{id}", test["id"])
            headers = {"Authorization": f"Bearer {test['token']}"}
            
            try:
                if method == "GET":
                    resp = requests.get(url, headers=headers, timeout=10)
                elif method == "DELETE":
                    # Cuidado: não executar DELETE real em produção
                    resp = requests.delete(url, headers=headers, timeout=10)
                elif method == "PATCH":
                    resp = requests.patch(url, headers=headers, json={}, timeout=10)
                else:
                    continue
                
                # Análise
                success = resp.status_code in [200, 201, 204]
                expected = test["should_succeed"]
                vulnerable = success and not expected
                
                result = {
                    "test": test["name"],
                    "method": method,
                    "url": url,
                    "status": resp.status_code,
                    "success": success,
                    "expected_success": expected,
                    "vulnerable": vulnerable,
                }
                
                # Tentar extrair dados sensíveis da resposta
                if vulnerable and resp.content:
                    try:
                        data = resp.json()
                        sensitive_fields = ["password", "passwordHash", "secret", "token", "apiKey", "creditCard"]
                        items = data if isinstance(data, list) else [data]
                        exposed = sorted({k for item in items if isinstance(item, dict) for k in item
                                          if any(s.lower() in k.lower() for s in sensitive_fields)})
                        if exposed:
                            result["exposed_fields"] = exposed
                    except ValueError:
                        pass
                
                results.append(result)
                
            except requests.exceptions.RequestException as e:
                results.append({
                    "test": test["name"],
                    "method": method,
                    "url": url,
                    "error": str(e),
                })
    
    return results


def test_uuid_manipulation(url_template: str, token: str, valid_id: str) -> list[dict]:
    """Testa manipulação de UUID/ID."""
    
    manipulation_tests = [
        ("UUID inválido", "*"),
        ("Path traversal", "../admin"),
        ("SQL injection", "1 OR 1=1"),
        ("SQL injection 2", "'; DROP TABLE users;--"),
        ("NoSQL injection", '{"$gt":""}'),
        ("Zero", "0"),
        ("Negativo", "-1"),
        ("Muito grande", "9" * 50),
    ]
    
    results = []
    headers = {"Authorization": f"Bearer {token}"}
    
    for name, payload in manipulation_tests:
        url = url_template.replace("{id}", payload)
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            
            # Erro 400/404 é esperado para IDs inválidos
            # 500 indica falta de validação (vulnerável)
            vulnerable = resp.status_code >= 500
            
            results.append({
                "test": name,
                "payload": payload,
                "status": resp.status_code,
                "vulnerable": vulnerable,
                "note": "Server error indica falta de validação" if vulnerable else "OK",
            })
            
        except Exception as e:
            results.append({
                "test": name,
                "payload": payload,
                "error": str(e),
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description="BOLA Vulnerability Tester")
    parser.add_argument("--url", required=True, help="URL com {id} placeholder")
    parser.add_argument("--token-a", required=True, help="Token do usuário A")
    parser.add_argument("--token-b", required=True, help="Token do usuário B")
    parser.add_argument("--id-a", required=True, help="ID do usuário A")
    parser.add_argument("--id-b", required=True, help="ID do usuário B")
    parser.add_argument("--methods", default="GET", help="Métodos HTTP (GET,PATCH,DELETE)")
    parser.add_argument("--test-manipulation", action="store_true", help="Testar manipulação de ID")
    parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")
    args = parser.parse_args()
    
    print("🔍 BOLA (Broken Object Level Authorization) Test")
    print("="*60)
    print(f"Target: {args.url}\n")
    
    methods = [m.strip().upper() for m in args.methods.split(",")]
    
    # Teste BOLA principal
    print("📋 Testando acesso cruzado entre usuários...\n")
    bola_results = test_bola(
        args.url,
        args.token_a,
        args.token_b,
        args.id_a,
        args.id_b,
        methods
    )
    
    vulnerabilities_found = [r for r in bola_results if r.get("vulnerable")]
    
    for r in bola_results:
        if r.get("error"):
            print(f"   ❓ {r['test']}: ERRO - {r['error']}")
        elif r.get("vulnerable"):
            print(f"   🔴 {r['test']}: VULNERÁVEL! Status {r['status']}")
            if r.get("exposed_fields"):
                print(f"      ⚠️  Campos sensíveis expostos: {r['exposed_fields']}")
        else:
            status = "✅" if r["success"] == r["expected_success"] else "⚠️"
            print(f"   {status} {r['test']}: Status {r['status']}")
    
    # Teste de manipulação de ID
    manipulation_results = []
    if args.test_manipulation:
        print("\n📋 Testando manipulação de ID...\n")
        manipulation_results = test_uuid_manipulation(args.url, args.token_a, args.id_a)
        
        for r in manipulation_results:
            if r.get("vulnerable"):
                print(f"   🔴 {r['test']}: VULNERÁVEL! Status {r['status']}")
            else:
                print(f"   ✅ {r['test']}: Status {r.get('status', 'N/A')}")
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    if vulnerabilities_found:
        print(f"\n🔴 VULNERABILIDADES ENCONTRADAS: {len(vulnerabilities_found)}")
        print("\n⚠️  RECOMENDAÇÕES:")
        print("   1. Implementar verificação de ownership em cada endpoint")
        print("   2. Validar que user.id === resource.ownerId")
        print("   3. Usar middleware de autorização centralizado")
    else:
        print("\n✅ Nenhuma vulnerabilidade BOLA encontrada")
    
    # Output JSON
    result = {
        "target": args.url,
        "bola_tests": bola_results,
        "manipulation_tests": manipulation_results,
        "vulnerable": len(vulnerabilities_found) > 0,
        "vulnerability_count": len(vulnerabilities_found),
    }
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Resultado salvo em: {args.output}")
    
    # Exit code não-zero se vulnerável
    sys.exit(1 if vulnerabilities_found else 0)


if __name__ == "__main__":
    main()
