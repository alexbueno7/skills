#!/usr/bin/env bash
# Wrapper curl para a API Audaks Cloud.
# Uso: audaks.sh METHOD /path [json-body]
#   audaks.sh GET /virtual-machines
#   audaks.sh POST /virtual-machines/vm-xxx/stop
#   audaks.sh POST /security-groups/sg-xxx/add-rule '{"direction":"ingress",...}'
set -euo pipefail
: "${AUDAKS_API_TOKEN:?defina AUDAKS_API_TOKEN (Perfil > API > Enable API no painel)}"
BASE="${AUDAKS_API_URL:-https://api.audaks.com.br/api}"
method="${1:?METHOD}"; path="${2:?/path}"; body="${3:-}"
args=(-sS -X "$method" "$BASE$path" -H "Authorization: Bearer $AUDAKS_API_TOKEN" -H "Accept: application/json")
[ -n "$body" ] && args+=(-H "Content-Type: application/json" --data "$body")
curl "${args[@]}" -w '\n%{http_code}\n' | { out=$(cat); code=${out##*$'\n'}; echo "${out%$'\n'*}" | (python3 -m json.tool 2>/dev/null || cat); [ "$code" -lt 400 ] || { echo "HTTP $code" >&2; exit 1; }; }
