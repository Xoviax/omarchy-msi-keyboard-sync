#!/usr/bin/env python3
from __future__ import annotations

import colorsys
import os
import re
import subprocess
from typing import List


MSI_MODEL_NAME = "GE75"  # Change this to your specific MSI laptop model if needed


def convert_hex_color_to_rgb_floats(
    hex_color_string: str,
) -> tuple[float, float, float]:
    normalized_hex_string = hex_color_string.strip().lower().lstrip("#")
    if not re.fullmatch(r"[0-9a-f]{6}", normalized_hex_string):
        raise ValueError(f"Invalid hex color: {hex_color_string}")

    red_value = int(normalized_hex_string[0:2], 16) / 255.0
    green_value = int(normalized_hex_string[2:4], 16) / 255.0
    blue_value = int(normalized_hex_string[4:6], 16) / 255.0
    return red_value, green_value, blue_value


def extract_hex_colors_from_text(text: str) -> List[str]:
    found_colors = re.findall(r"#?[0-9a-fA-F]{6}", text)

    seen_colors: set[str] = set()
    unique_colors: List[str] = []
    for found_color in found_colors:
        normalized_color = found_color.lower().lstrip("#")
        if normalized_color not in seen_colors:
            seen_colors.add(normalized_color)
            unique_colors.append(normalized_color)

    return unique_colors


def choose_most_colorful_hex_color(hex_color_list: List[str]) -> str:
    scored_candidates = []

    for hex_color in hex_color_list:
        try:
            red_value, green_value, blue_value = convert_hex_color_to_rgb_floats(hex_color)
        except ValueError:
            continue

        hue_value, saturation_value, brightness_value = colorsys.rgb_to_hsv(red_value, green_value, blue_value)

        # Ignore pure black/white-ish values (these are never "most colorful")
        # White has saturation ~0, black has brightness ~0.
        if brightness_value < 0.05:
            continue
        if saturation_value < 0.05 and brightness_value > 0.90:
            continue

        # Prefer saturation, but keep visibility
        # This will still allow darker themes to pick a real accent color.
        score = (saturation_value * 1.5) + (brightness_value * 0.4)

        scored_candidates.append((score, saturation_value, brightness_value, hex_color))

    if not scored_candidates:
        print("No usable colors extracted; keeping keyboard unchanged.")
        return ""

    scored_candidates.sort(reverse=True, key=lambda item: item[0])

    # Debug: show top 8 candidates
    print("Top candidates (score, sat, val, hex):")
    for candidate in scored_candidates[:8]:
        print(candidate)

    chosen = scored_candidates[0][3].lower().lstrip("#")
    print(f"Chosen color: {chosen}")
    return chosen


def set_msi_keyboard_color(hex_color: str) -> None:
    normalized_color = hex_color.lower().lstrip("#")
    subprocess.run(
        ["msi-perkeyrgb", "--model", MSI_MODEL_NAME, "-s", normalized_color],
        check=False,
    )


def main() -> None:
    candidate_paths = [
        os.path.expanduser("~/.config/omarchy/current/theme/alacritty.toml"),
        os.path.expanduser("~/.config/alacritty/alacritty.toml"),
    ]

    alacritty_config_path = next(
        (path for path in candidate_paths if os.path.isfile(path)),
        "",
    )
    if not alacritty_config_path:
        return
    
    if not os.path.isfile(alacritty_config_path):
        # Fallback: do nothing noisy if the file is missing
        return

    config_text = open(alacritty_config_path, "r", encoding="utf-8").read()
    extracted_colors = extract_hex_colors_from_text(config_text)
    chosen_color = choose_most_colorful_hex_color(extracted_colors)
    set_msi_keyboard_color(chosen_color)

    chosen_color = choose_most_colorful_hex_color(extracted_colors)
    if chosen_color:
        set_msi_keyboard_color(chosen_color)
    else:
        return


if __name__ == "__main__":
    main()
