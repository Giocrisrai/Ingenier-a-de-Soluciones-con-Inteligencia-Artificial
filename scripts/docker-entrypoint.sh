#!/usr/bin/env sh
set -eu
cd /workspace
uv sync
exec uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
