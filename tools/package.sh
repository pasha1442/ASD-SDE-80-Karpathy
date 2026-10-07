#!/usr/bin/env bash
# Build dist/ste-explain.zip for upload to the Claude app (Customize > Skills).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 skills/ste-explain/scripts/ste_check.py --selftest
rm -f dist/ste-explain.zip
mkdir -p dist
(cd skills && zip -r -q ../dist/ste-explain.zip ste-explain -x '*/__pycache__/*' '*.pyc' '*.DS_Store')
echo "Built dist/ste-explain.zip"
unzip -l dist/ste-explain.zip | tail -1
