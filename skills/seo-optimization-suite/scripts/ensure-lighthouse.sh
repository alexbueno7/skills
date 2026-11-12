#!/usr/bin/env bash
# Verifica/instala Lighthouse CLI globalmente
set -euo pipefail

export PATH="${NVM_DIR:+$NVM_DIR/versions/node/*/bin:}${HOME}/.nvm/versions/node/v24.15.0/bin:${PATH}"

if command -v lighthouse >/dev/null 2>&1; then
  echo "Lighthouse $(lighthouse --version) — OK"
  exit 0
fi

echo "Instalando Lighthouse globalmente via npm..." >&2
npm install -g lighthouse@latest
echo "Lighthouse $(lighthouse --version) instalado."

if ! command -v google-chrome >/dev/null 2>&1 && ! command -v chromium >/dev/null 2>&1; then
  echo "AVISO: Chrome/Chromium não encontrado. Lighthouse precisa de um browser Chromium." >&2
  echo "  Ubuntu/Debian: sudo apt install google-chrome-stable" >&2
  exit 1
fi
