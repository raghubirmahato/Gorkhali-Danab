#!/usr/bin/env bash
# Regenerates every SVG and PNG in logo/.
# Needs: python3 with fonttools + uharfbuzz, node with playwright.
set -euo pipefail
cd "$(dirname "$0")"
[ -f fonts/cinzel-900.ttf ] && [ -f fonts/eczar-800.ttf ] || ./fetch-fonts.sh
python3 lockup.py ..
r() { node render.js "../$1.svg" "../png/$1-$2.png" "$2"; echo "png/$1-$2.png"; }
r gorkhali-danab-logo 1024
r gorkhali-danab-logo 2048
r gorkhali-danab-logo-dark 1024
r gorkhali-danab-logo-dark 2048
r gorkhali-danab-horizontal 1600
r gorkhali-danab-horizontal 3200
r gorkhali-danab-horizontal-dark 1600
r gorkhali-danab-horizontal-dark 3200
for s in 32 64 180 512 1024 2048; do r gorkhali-danab-emblem $s; done
