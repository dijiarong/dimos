#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "================================================================"
echo " verify.sh @ $REPO_ROOT"
echo " host: $(uname -srm)"
echo "================================================================"

# Bootstrap-friendly: 空仓库阶段如果还没有 pyproject.toml，就先跳过 Python 验证。
if [[ ! -f "pyproject.toml" ]]; then
  echo ">>> [1/1] pyproject.toml not found, skip uv sync + pytest for bootstrap"
  echo "<<< OK"
  exit 0
fi

echo ">>> [1/2] uv sync --all-extras"
uv sync --all-extras
echo "<<< OK"

echo ">>> [2/2] uv run pytest -q"
uv run pytest -q
echo "<<< OK"
