# Omarchy MSI Keyboard Sync

Omarchy MSI Keyboard Sync is a small utility that synchronizes an MSI laptop’s keyboard backlight color with the currently active Omarchy theme. When the theme changes, the keyboard updates automatically to match the theme’s palette.

## Key Features
- Automatically updates the keyboard backlight on Omarchy theme changes (via Omarchy hooks).
- Selects a “most colorful” (high-saturation) accent-like color from the theme palette.
- Works with MSI models supported by `msi-perkeyrgb`.
- Extracts colors from the active theme’s `alacritty.toml`.

## Requirements
- Python 3.x
- Omarchy hooks enabled/working
- `msi-perkeyrgb` (see: https://github.com/Askannz/msi-perkeyrgb)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Xoviax/omarchy-msi-keyboard-sync.git
   cd omarchy-msi-keyboard-sync
2. Install 'msi-perkeyrgb' by following the instructions on its GitHub page.
3. Set your MSI model (if needed, currently set to GE75):
    - Edit 'src/omarchy-keyboard-theme-sync.py' and update 'MSI_MODEL_NAME' variable (example: `MSI_MODEL_NAME = "GT63"`).
4. Install the hook + script:
    ```bash
    ./install.sh

## How It Works
- Omarchy triggers the 'theme-set' hook when the theme changes.
- The python script reads the active theme palette from: ~/.config/omarchy/current/theme/alacritty.toml'
and applies the selected color using 'msi-perkeyrgb'.

## Testing
- Simulate a theme change by running:
    ```bash
    ~/.config/omarchy/hooks/theme-set test-theme
- Manually set a color by running:
    ```bash
    msi-perkeyrgb --model <model> -s <ffffff>

