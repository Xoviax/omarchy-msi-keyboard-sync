#!/usr/bin/env bash
set -euo pipefail

# Install locations
BIN_DIR="$HOME/.local/bin"
HOOKS_DIR="$HOME/.config/omarchy/hooks"
HOOKS_SUBDIR="$HOOKS_DIR/theme-set.d"

mkdir -p "$BIN_DIR" "$HOOKS_SUBDIR"

# Copy files
install -m 0755 "src/omarchy-keyboard-theme-sync.py" "$BIN_DIR/omarchy-keyboard-theme-sync.py"
install -m 0755 "hooks/theme-set" "$HOOKS_DIR/theme-set"
install -m 0755 "hooks/theme-set.d/60-msi-keyboard-sync.sh" "$HOOKS_SUBDIR/60-msi-keyboard-sync.sh"

echo "Installed:"
echo "  $BIN_DIR/omarchy-keyboard-theme-sync.py"
echo "  $HOOKS_DIR/theme-set"
echo "  $HOOKS_SUBDIR/60-msi-keyboard-sync.sh"
echo
echo "Test:"
echo "  $HOOKS_DIR/theme-set test-theme"
