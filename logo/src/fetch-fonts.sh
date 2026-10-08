#!/usr/bin/env bash
# Downloads the two typefaces the wordmark is outlined from (both SIL Open Font License).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fonts
fetch() {
  url=$(curl -fsS "https://fonts.googleapis.com/css2?family=$1" | grep -o 'https://[^)]*\.ttf' | head -1)
  curl -fsS -o "fonts/$2" "$url"
  echo "fonts/$2"
}
fetch "Cinzel:wght@900" cinzel-900.ttf
fetch "Eczar:wght@800" eczar-800.ttf
