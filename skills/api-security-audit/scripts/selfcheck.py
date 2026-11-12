#!/usr/bin/env python3
"""
Self-check dos scripts desta pasta, sem rede (requests é substituído por dublês).

Uso: python selfcheck.py
"""

import contextlib
import io
import sys
from types import SimpleNamespace
from unittest import mock

import bola_test
import endpoint_scan
import rate_limit_test


def resp(status=200, body=None):
    return SimpleNamespace(status_code=status, content=b"x", headers={}, json=lambda: body)


# 1. rate_limit_test: relatório não quebra com status int e str misturados
mixed = iter([resp(200), rate_limit_test.requests.exceptions.ConnectionError("down"), resp(429)])


def fake_get(*a, **k):
    r = next(mixed)
    if isinstance(r, Exception):
        raise r
    return r


with mock.patch.object(rate_limit_test.requests, "get", fake_get), \
        mock.patch.object(sys, "argv", ["x", "--url", "http://t.test", "--requests", "3", "--concurrent", "1"]), \
        contextlib.redirect_stdout(io.StringIO()) as out, contextlib.suppress(SystemExit):
    rate_limit_test.main()
assert "error" in out.getvalue() and "429" in out.getvalue(), out.getvalue()

# 2. bola_test: em DELETE os acessos cruzados vêm antes dos legítimos
order = []
with mock.patch.object(bola_test.requests, "delete", lambda url, **k: order.append(url) or resp(403)), \
        contextlib.redirect_stdout(io.StringIO()):
    res = bola_test.test_bola("http://t.test/{id}", "ta", "tb", "A", "B", ["DELETE"])
assert [r["expected_success"] for r in res] == [False, False, True, True], res

# 3. bola_test: campo sensível é achado em resposta que é lista
with mock.patch.object(bola_test.requests, "get", lambda url, **k: resp(200, [{"id": 1, "passwordHash": "h"}])), \
        contextlib.redirect_stdout(io.StringIO()):
    res = bola_test.test_bola("http://t.test/{id}", "ta", "tb", "A", "B", ["GET"])
assert [r.get("exposed_fields") for r in res if r["vulnerable"]] == [["passwordHash"]] * 2, res


# 4. endpoint_scan: Ctrl+C durante a busca do OpenAPI não é engolido
def interrupt(*a, **k):
    raise KeyboardInterrupt


with mock.patch.object(endpoint_scan.requests, "get", interrupt), contextlib.redirect_stdout(io.StringIO()):
    try:
        endpoint_scan.analyze_openapi("http://t.test")
        raise AssertionError("KeyboardInterrupt foi engolido")
    except KeyboardInterrupt:
        pass

print("selfcheck ok")
