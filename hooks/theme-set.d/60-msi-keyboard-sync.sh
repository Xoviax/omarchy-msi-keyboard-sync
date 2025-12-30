#!/usr/bin/env bash
set -euo pipefail

theme_name="${1:-unknown}"

# Log the theme change
log_file="$HOME/.local/state/omarchy-keyboard-sync.log"
mkdir -p "$(dirname "$log_file")"
echo "[$(date -Is)] Theme changed: $theme_name" >> "$log_file"

# Run the Python color picker + keyboard setter
"$HOME/.local/bin/omarchy-keyboard-theme-sync.py" >> "$log_file" 2>&1 || true
