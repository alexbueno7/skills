#!/usr/bin/env bash
# Checagens HTTP de indexação — seo-optimization-suite
# Uso: technical-seo-check.sh <URL canônica, preferir https://dominio.com.br>
set -euo pipefail

URL="${1:-}"
[[ -n "$URL" ]] || { echo "Uso: technical-seo-check.sh https://dominio.com.br" >&2; exit 1; }

URL="${URL%/}"
HOST="${URL#*://}"
HOST="${HOST%%/*}"
SCHEME="${URL%%://*}"

apex="$HOST"
if [[ "$HOST" == www.* ]]; then
  apex="${HOST#www.}"
fi
www="www.$apex"

headers() {
  curl -sI -L --max-redirs 0 --max-time 20 "$1" 2>/dev/null | tr -d '\r' | head -n 20
}

status_of() {
  curl -sI --max-time 20 "$1" 2>/dev/null | tr -d '\r' | awk 'BEGIN{s=""} /^HTTP/{s=$2} END{print s}'
}

body_ok() {
  local code
  code="$(status_of "$1")"
  [[ "$code" == "200" ]]
}

echo "=== technical-seo-check ==="
echo "input: $URL"
echo "apex:  $apex"
echo "www:   $www"
echo

pass=0
fail=0
na=0

check() {
  local label="$1" ok="$2" detail="$3"
  if [[ "$ok" == "pass" ]]; then
    echo "PASS  $label — $detail"
    pass=$((pass + 1))
  elif [[ "$ok" == "na" ]]; then
    echo "N/A   $label — $detail"
    na=$((na + 1))
  else
    echo "FAIL  $label — $detail"
    fail=$((fail + 1))
  fi
}

robots_url="${SCHEME}://${apex}/robots.txt"
sitemap_url="${SCHEME}://${apex}/sitemap.xml"
sitemap_idx_url="${SCHEME}://${apex}/sitemap_index.xml"

if body_ok "$robots_url"; then
  robots_body="$(curl -s --max-time 20 "$robots_url")"
  if echo "$robots_body" | grep -qiE '^sitemap:'; then
    check "robots.txt" pass "$robots_url (tem Sitemap:)"
  else
    check "robots.txt" fail "$robots_url 200 mas sem linha Sitemap:"
  fi
else
  check "robots.txt" fail "$robots_url status=$(status_of "$robots_url")"
fi

if body_ok "$sitemap_url"; then
  check "sitemap.xml" pass "$sitemap_url"
elif body_ok "$sitemap_idx_url"; then
  check "sitemap.xml" pass "$sitemap_idx_url (index)"
else
  check "sitemap.xml" fail "nem /sitemap.xml nem /sitemap_index.xml em 200"
fi

apex_url="${SCHEME}://${apex}/"
www_url="${SCHEME}://${www}/"
apex_code="$(status_of "$apex_url")"
www_headers="$(headers "$www_url")"
www_code="$(echo "$www_headers" | awk 'BEGIN{s=""} /^HTTP/{s=$2} END{print s}')"
www_loc="$(echo "$www_headers" | awk 'BEGIN{IGNORECASE=1} /^location:/{print $2; exit}')"

if [[ "$apex_code" == "200" ]]; then
  check "apex 200" pass "$apex_url → $apex_code"
else
  check "apex 200" fail "$apex_url → $apex_code (canônico esperado = apex)"
fi

if [[ "$www_code" =~ ^30 ]] && echo "$www_loc" | grep -q "$apex"; then
  check "www → apex 301" pass "$www_url $www_code → $www_loc"
else
  check "www → apex 301" fail "$www_url status=$www_code location=${www_loc:-none}"
fi

https_code="$(status_of "https://${apex}/")"
if [[ "$https_code" == "200" ]]; then
  check "https" pass "https://${apex}/ → 200"
else
  check "https" fail "https://${apex}/ → $https_code"
fi

llms="${SCHEME}://${apex}/llms.txt"
if body_ok "$llms"; then
  check "llms.txt" pass "$llms"
else
  check "llms.txt" fail "$llms status=$(status_of "$llms")"
fi

openapi_json="${SCHEME}://${apex}/openapi.json"
openapi_yaml="${SCHEME}://${apex}/openapi.yaml"
if body_ok "$openapi_json"; then
  check "openapi.json" pass "$openapi_json"
elif body_ok "$openapi_yaml"; then
  check "openapi.json" pass "$openapi_yaml"
else
  check "openapi.json" na "sem /openapi.json nem /openapi.yaml (N/A se o site não tem API pública)"
fi

echo
echo "resumo: PASS=$pass FAIL=$fail N/A=$na"
echo "GSC/Bing, submissão de sitemap, backlinks e Cloudflare SSL: ver references/full-audit-checklist.md (HUMAN)"
exit 0
