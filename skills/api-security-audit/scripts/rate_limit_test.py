#!/usr/bin/env python3
"""
Rate Limiting Tester
Verifica se a API implementa rate limiting adequado.

Uso: python rate_limit_test.py --url https://api.example.com/login \
                               --requests 100 \
                               --method POST
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

try:
    import requests
except ImportError:
    print("Erro: requests não instalado. Execute: pip install requests")
    sys.exit(1)


def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    request_num: int = 0
) -> dict:
    """Faz uma única requisição e retorna métricas."""
    
    start = time.time()
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=data or {}, timeout=30)
        else:
            resp = requests.request(method, url, headers=headers, json=data, timeout=30)
        
        elapsed = time.time() - start
        
        return {
            "request_num": request_num,
            "status": resp.status_code,
            "time": round(elapsed, 3),
            "rate_limited": resp.status_code == 429,
            "retry_after": resp.headers.get("Retry-After"),
            "ratelimit_remaining": resp.headers.get("X-RateLimit-Remaining"),
        }
        
    except requests.exceptions.Timeout:
        return {
            "request_num": request_num,
            "status": "timeout",
            "time": time.time() - start,
        }
    except Exception as e:
        return {
            "request_num": request_num,
            "status": "error",
            "error": str(e),
        }


def test_rate_limiting(
    url: str,
    num_requests: int = 100,
    method: str = "GET",
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    concurrent: int = 10,
    delay: float = 0
) -> dict:
    """
    Executa múltiplas requisições para testar rate limiting.
    """
    
    results = []
    rate_limited_at = None
    
    print(f"🚀 Enviando {num_requests} requisições...")
    
    if concurrent > 1:
        # Requisições paralelas
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            futures = []
            for i in range(num_requests):
                futures.append(
                    executor.submit(make_request, url, method, headers, data, i)
                )
                if delay > 0:
                    time.sleep(delay)
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                # Primeira vez que foi limitado
                if result.get("rate_limited") and rate_limited_at is None:
                    rate_limited_at = result["request_num"]
                
                # Progress
                done = len(results)
                if done % 20 == 0:
                    print(f"   Progresso: {done}/{num_requests}")
    else:
        # Requisições sequenciais
        for i in range(num_requests):
            result = make_request(url, method, headers, data, i)
            results.append(result)
            
            if result.get("rate_limited") and rate_limited_at is None:
                rate_limited_at = i
            
            if (i + 1) % 20 == 0:
                print(f"   Progresso: {i + 1}/{num_requests}")
            
            if delay > 0:
                time.sleep(delay)
    
    # Ordenar por número da requisição
    results.sort(key=lambda x: x.get("request_num", 0))
    
    # Análise
    status_counts = {}
    total_time = 0
    for r in results:
        status = r.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        total_time += r.get("time", 0)
    
    rate_limited_count = sum(1 for r in results if r.get("rate_limited"))
    
    return {
        "url": url,
        "method": method,
        "total_requests": num_requests,
        "concurrent": concurrent,
        "status_distribution": status_counts,
        "rate_limited_count": rate_limited_count,
        "rate_limited_at": rate_limited_at,
        "avg_response_time": round(total_time / len(results), 3) if results else 0,
        "has_rate_limiting": rate_limited_count > 0,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Rate Limiting Tester")
    parser.add_argument("--url", required=True, help="URL para testar")
    parser.add_argument("--requests", "-n", type=int, default=100, help="Número de requisições")
    parser.add_argument("--method", "-m", default="GET", help="Método HTTP")
    parser.add_argument("--concurrent", "-c", type=int, default=10, help="Requisições paralelas")
    parser.add_argument("--delay", "-d", type=float, default=0, help="Delay entre requisições (segundos)")
    parser.add_argument("--token", help="Bearer token")
    parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")
    args = parser.parse_args()
    
    print("⏱️  Rate Limiting Test")
    print("="*60)
    print(f"Target: {args.url}")
    print(f"Requisições: {args.requests}")
    print(f"Concorrência: {args.concurrent}")
    print("="*60 + "\n")
    
    headers = {}
    if args.token:
        headers["Authorization"] = f"Bearer {args.token}"
    
    # Dados fake para POST
    data = {"email": "test@test.com", "password": "wrongpassword"}
    
    result = test_rate_limiting(
        args.url,
        args.requests,
        args.method,
        headers,
        data if args.method == "POST" else None,
        args.concurrent,
        args.delay
    )
    
    # Resultado
    print("\n" + "="*60)
    print("📊 RESULTADO")
    print("="*60)
    
    print(f"\n📈 Distribuição de Status:")
    for status, count in sorted(result["status_distribution"].items(), key=lambda kv: str(kv[0])):
        pct = (count / args.requests) * 100
        bar = "█" * int(pct / 5)
        print(f"   {status:>4}: {count:>4} ({pct:5.1f}%) {bar}")
    
    print(f"\n⏱️  Tempo médio de resposta: {result['avg_response_time']}s")
    
    if result["has_rate_limiting"]:
        print(f"\n✅ Rate limiting DETECTADO!")
        print(f"   Primeira limitação após: {result['rate_limited_at']} requisições")
        print(f"   Total de 429s: {result['rate_limited_count']}")
    else:
        print(f"\n🔴 VULNERÁVEL! Sem rate limiting detectado após {args.requests} requisições")
        print("\n⚠️  RECOMENDAÇÕES:")
        print("   1. Implementar rate limiting (100-200 req/min para auth)")
        print("   2. Usar biblioteca como fastify-rate-limit ou express-rate-limit")
        print("   3. Considerar rate limit por IP e por usuário")
        print("   4. Adicionar headers X-RateLimit-Remaining")
    
    if args.output:
        # Não salvar todos os resultados individuais (muito grande)
        output_data = {k: v for k, v in result.items() if k != "results"}
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\n💾 Resultado salvo em: {args.output}")
    
    # Exit code
    sys.exit(0 if result["has_rate_limiting"] else 1)


if __name__ == "__main__":
    main()
