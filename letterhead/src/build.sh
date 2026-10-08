#!/usr/bin/env bash
# Rebuilds Gorkhali-Danab-Letterhead.docx. Needs node with the docx package.
set -euo pipefail
cd "$(dirname "$0")"
node make.js . ../Gorkhali-Danab-Letterhead.docx
