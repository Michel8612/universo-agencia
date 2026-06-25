#!/usr/bin/env bash
# NEXIA — Instala y activa GitHub Spec Kit en este repo (para Claude Code).
# Ejecutar desde la RAÍZ del repo, en tu PC (no funciona en la nube por la red).
#   bash mundo-agencia/setup-speckit.sh
set -euo pipefail

SPECKIT_VERSION="v0.11.8"

echo "==> Comprobando uv..."
if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: falta 'uv'. Instálalo: https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

echo "==> Instalando specify-cli ($SPECKIT_VERSION)..."
uv tool install specify-cli --from "git+https://github.com/github/spec-kit.git@$SPECKIT_VERSION" \
  || uv tool upgrade specify-cli \
  || true

# Detectar tipo de script segun el SO
SCRIPT_TYPE="sh"
case "${OS:-}" in
  Windows_NT) SCRIPT_TYPE="ps" ;;
esac

echo "==> Inicializando Spec Kit en el directorio actual (integration=claude, script=$SCRIPT_TYPE)..."
specify init --here --integration claude --script "$SCRIPT_TYPE" --force

echo ""
echo "==> Listo. En Claude Code ya tienes: /speckit.constitution, /speckit.specify,"
echo "    /speckit.plan, /speckit.tasks, /speckit.implement"
echo "    Constitución sugerida: ver mundo-agencia/SPECKIT.md"
