#!/usr/bin/env bash
# Lighthouse CLI audit — seo-optimization-suite
# Uso: lighthouse-audit.sh <URL> [--desktop] [--output-dir DIR]
set -euo pipefail

FORM_FACTOR="mobile"
OUTPUT_DIR=""
URL=""

usage() {
  cat <<'EOF'
Uso: lighthouse-audit.sh <URL> [opções]

Opções:
  --desktop       Rodar também audit desktop (além de mobile)
  --output-dir D  Diretório de saída (default: ./.lighthouse-reports)
  -h, --help      Mostrar esta ajuda

Exemplos:
  lighthouse-audit.sh https://www.exemplo.com.br
  lighthouse-audit.sh http://127.0.0.1:8000 --output-dir /tmp/lh
  lighthouse-audit.sh https://www.exemplo.com.br --desktop
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --desktop) FORM_FACTOR="both"; shift ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Opção desconhecida: $1" >&2; usage; exit 1 ;;
    *)
      if [[ -z "$URL" ]]; then URL="$1"; else echo "URL extra: $1" >&2; exit 1; fi
      shift
      ;;
  esac
done

[[ -n "$URL" ]] || { echo "URL obrigatória." >&2; usage; exit 1; }

# Garantir Node/nvm no PATH (Lighthouse instalado globalmente via npm)
export PATH="${NVM_DIR:+$NVM_DIR/versions/node/*/bin:}${HOME}/.nvm/versions/node/v24.15.0/bin:${PATH}"

if ! command -v lighthouse >/dev/null 2>&1; then
  echo "Lighthouse não encontrado. Instalando globalmente..." >&2
  npm install -g lighthouse@latest
fi

LH_VERSION="$(lighthouse --version 2>/dev/null || echo unknown)"
echo "Lighthouse ${LH_VERSION}"

OUTPUT_DIR="${OUTPUT_DIR:-./.lighthouse-reports}"
mkdir -p "$OUTPUT_DIR"

SLUG="$(echo "$URL" | sed -E 's|https?://||' | tr '/:?&=.' '_' | tr -s '_' | sed 's/^_*//;s/_*$//')"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CHROME_FLAGS="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"

run_audit() {
  local factor="$1"
  local label="$2"
  local base_path="${OUTPUT_DIR}/${SLUG}-${label}-${TIMESTAMP}"
  local json_path="${base_path}.report.json"
  local html_path="${base_path}.report.html"

  echo ""
  echo "=== Lighthouse ${label} — ${URL} ==="

  local extra_args=()
  if [[ "$factor" == "mobile" ]]; then
    extra_args+=(--form-factor=mobile --screenEmulation.mobile=true)
  else
    extra_args+=(--preset=desktop)
  fi

  if ! lighthouse "$URL" \
    "${extra_args[@]}" \
    --only-categories=performance,seo,accessibility,best-practices \
    --output=json \
    --output=html \
    --output-path="$base_path" \
    --chrome-flags="$CHROME_FLAGS" \
    --quiet; then
    echo "ERRO: Lighthouse falhou para ${label}. Verifique URL, SSL e se o servidor responde." >&2
    return 1
  fi

  if [[ ! -f "$json_path" ]]; then
    echo "ERRO: JSON não gerado em ${json_path}" >&2
    return 1
  fi

  node -e "
    const r = require('${json_path}');
    const s = (id) => Math.round((r.categories[id]?.score ?? 0) * 100);
    const audit = (id) => r.audits[id]?.displayValue ?? '—';
    console.log('Performance:     ' + s('performance'));
    console.log('SEO:             ' + s('seo'));
    console.log('Accessibility:   ' + s('accessibility'));
    console.log('Best Practices:  ' + s('best-practices'));
    console.log('LCP:             ' + audit('largest-contentful-paint'));
    console.log('FCP:             ' + audit('first-contentful-paint'));
    console.log('CLS:             ' + audit('cumulative-layout-shift'));
    console.log('TBT:             ' + audit('total-blocking-time'));
    console.log('TTFB:            ' + audit('server-response-time'));
    console.log('');
    console.log('Relatórios:');
    console.log('  JSON: ${json_path}');
    console.log('  HTML: ${html_path}');
  "
}

run_audit mobile mobile
if [[ "$FORM_FACTOR" == "both" ]]; then
  run_audit desktop desktop
fi

echo ""
echo "Auditoria concluída. Relatórios em: ${OUTPUT_DIR}"
