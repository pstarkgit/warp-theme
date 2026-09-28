#!/usr/bin/env python3
"""Generate the Afterlight Warp themes and their glow wallpapers on macOS."""

import math
import struct
import subprocess
import zlib
from pathlib import Path


HERE = Path(__file__).parent
WIDTH, HEIGHT = 960, 600

THEMES = [
    {
        "slug": "aurora-tide",
        "name": "Aurora Tide",
        "base": "#091316",
        "foreground": "#E5F5EF",
        "accent": ("#5CCDB5", "#A6E3D3"),
        "cursor": "#B6F4DF",
        "glows": [
            ("#3EE0BA", 0.12, 0.20, 0.25, 0.38, 0.54),
            ("#87B5FC", 0.88, 0.13, 0.22, 0.31, 0.48),
            ("#B18AF4", 0.84, 0.94, 0.37, 0.22, 0.35),
        ],
        "normal": ["#152226", "#E17C87", "#76CBA8", "#D6C278", "#7DAFE0", "#AB91D8", "#72D2D6", "#C7DDD8"],
        "bright": ["#627579", "#F4A4A6", "#A3E4C2", "#F2DFA2", "#A7CDF5", "#D1B4F2", "#A2EAEB", "#F1FAF5"],
    },
    {
        "slug": "aurora-prism",
        "name": "Aurora Prism",
        "wallpaper_opacity": 20,
        "base": "#0C0D1C",
        "foreground": "#EEEFFD",
        "accent": ("#86B5FF", "#DBA6F7"),
        "cursor": "#F4C8F4",
        "glows": [
            ("#69B9FF", 0.05, 0.16, 0.24, 0.36, 0.55),
            ("#A186F7", 0.78, 0.10, 0.33, 0.29, 0.49),
            ("#EE82BA", 0.94, 0.82, 0.34, 0.37, 0.41),
        ],
        "normal": ["#191A35", "#E48AA8", "#8CCDB9", "#DCC595", "#86B5FA", "#B49AEF", "#83CADF", "#D5D7ED"],
        "bright": ["#666981", "#F6B2CC", "#B0EAD6", "#F4DCB2", "#AFD0FF", "#D8BDFC", "#AFEAF4", "#F9F7FF"],
    },
    {
        "slug": "aurora-canopy",
        "name": "Aurora Canopy",
        "base": "#0D1510",
        "foreground": "#ECF2E5",
        "accent": ("#A7D774", "#71CDB1"),
        "cursor": "#D8EDA2",
        "glows": [
            ("#99E274", 0.11, 0.25, 0.28, 0.39, 0.48),
            ("#4ED5AE", 0.84, 0.18, 0.26, 0.36, 0.43),
            ("#E4D475", 0.91, 0.96, 0.36, 0.25, 0.31),
        ],
        "normal": ["#1B291F", "#DB8B7D", "#A1D284", "#DDC87C", "#8FAFD2", "#B5A0C8", "#79C9B3", "#D7E1CF"],
        "bright": ["#718070", "#EEB0A2", "#C4E7A6", "#F2E2A2", "#B3CBE9", "#D6BBE5", "#A4E8D4", "#F7F9EB"],
    },
    {
        "slug": "orchid-haze",
        "name": "Orchid Haze",
        "base": "#15101A",
        "foreground": "#F4EBF5",
        "accent": ("#D68EDE", "#F3ADC8"),
        "cursor": "#FFD1E8",
        "glows": [
            ("#B87BEE", 0.13, 0.17, 0.29, 0.31, 0.48),
            ("#EE88C3", 0.95, 0.52, 0.31, 0.45, 0.45),
            ("#777DDC", 0.54, 1.03, 0.43, 0.20, 0.26),
        ],
        "normal": ["#2A2030", "#E888A9", "#A6C99E", "#D9B689", "#9CA9DC", "#C797D6", "#87BFC7", "#E1D3E3"],
        "bright": ["#82728A", "#F5B2CA", "#C8E4BB", "#F1D5AC", "#C0C9EF", "#E9BDF2", "#AEE2E4", "#FFF5FF"],
    },
    {
        "slug": "solar-ember",
        "name": "Solar Ember",
        "wallpaper_opacity": 20,
        "base": "#170F0B",
        "foreground": "#F8EDE0",
        "accent": ("#EC874F", "#F5BE75"),
        "cursor": "#FFD393",
        "glows": [
            ("#F4773E", 0.08, 0.18, 0.27, 0.37, 0.48),
            ("#F9B35D", 0.95, 0.83, 0.38, 0.39, 0.45),
            ("#C6687B", 0.62, 0.01, 0.39, 0.22, 0.25),
        ],
        "normal": ["#2D1D17", "#E77A67", "#9EC198", "#E7B76F", "#88A9C4", "#C694AD", "#82C0BA", "#E5D2BE"],
        "bright": ["#8D7160", "#F5A48B", "#C0DBAE", "#FFD799", "#AEC9DF", "#E2B5CC", "#A9E1D7", "#FFF5E7"],
    },
    {
        "slug": "ember-focus",
        "name": "Ember Focus",
        "wallpaper_opacity": 20,
        "base": "#111113",
        "foreground": "#E7E3DD",
        "accent": ("#C66B32", "#E48C48"),
        "cursor": "#E9A061",
        "glows": [
            ("#95502F", 0.02, 0.16, 0.27, 0.35, 0.33),
            ("#C9773C", 1.02, 0.91, 0.37, 0.34, 0.34),
            ("#445366", 0.82, 0.04, 0.42, 0.28, 0.19),
        ],
        "normal": ["#252427", "#C7736B", "#91AD88", "#C7A16C", "#829EB2", "#AC8DA9", "#83AAA7", "#CDC9C3"],
        "bright": ["#777276", "#E99A88", "#B0C9A5", "#E2BF86", "#A7BFD0", "#C9A9C4", "#A4C9C3", "#F5F1EA"],
    },
]


def rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def png_bytes(theme):
    base = rgb(theme["base"])
    glows = [(rgb(color), x, y, sx, sy, strength)
             for color, x, y, sx, sy, strength in theme["glows"]]
    rows = bytearray()
    for iy in range(HEIGHT):
        y = iy / HEIGHT
        rows.append(0)
        for ix in range(WIDTH):
            x = ix / WIDTH
            color = [float(v) for v in base]
            for hue, cx, cy, sx, sy, strength in glows:
                dx = (x - cx) / sx
                dy = (y - cy) / sy
                light = 1.95 * strength * math.exp(-1.8 * (dx * dx + dy * dy))
                for channel in range(3):
                    color[channel] += (hue[channel] - color[channel]) * light
            if theme["slug"].startswith("aurora"):
                phase = {"aurora-tide": 0.0, "aurora-prism": 1.4, "aurora-canopy": 2.7}[theme["slug"]]
                ridge = 0.11 + 0.08 * math.sin(x * 6.2 + phase) + 0.027 * math.sin(x * 14 + phase)
                ribbon = 0.34 * math.exp(-((y - ridge) / 0.055) ** 2)
                ribbon *= math.exp(-((x - 0.5) / 0.58) ** 4)
                hue = glows[0][0]
                for channel in range(3):
                    color[channel] += (hue[channel] - color[channel]) * ribbon
            # Keep the middle of the terminal especially dark for readable text.
            center = math.exp(-((x - 0.48) / 0.34) ** 4 - ((y - 0.52) / 0.40) ** 4)
            color = [v * (1 - center * 0.15) for v in color]
            rows.extend(max(0, min(255, round(v))) for v in color)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


def yaml_text(theme):
    lines = [
        f"name: Afterlight - {theme['name']}",
        "accent:",
        f"  left: '{theme['accent'][0]}'",
        f"  right: '{theme['accent'][1]}'",
        f"cursor: '{theme['cursor']}'",
        f"background: '{theme['base']}'",
        f"foreground: '{theme['foreground']}'",
        "details: darker",
        "background_image:",
        f"  path: afterlight-{theme['slug']}.jpg",
        f"  opacity: {theme.get('wallpaper_opacity', 72)}",
        "terminal_colors:",
    ]
    for key in ("normal", "bright"):
        lines.append(f"  {key}:")
        for name, color in zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), theme[key]):
            lines.append(f"    {name}: '{color}'")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    for theme in THEMES:
        png_path = HERE / f"afterlight-{theme['slug']}.png"
        jpg_path = HERE / f"afterlight-{theme['slug']}.jpg"
        png_path.write_bytes(png_bytes(theme))
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88",
             str(png_path), "--out", str(jpg_path)],
            check=True,
            capture_output=True,
        )
        (HERE / f"afterlight-{theme['slug']}.yaml").write_text(yaml_text(theme))
        print(f"Afterlight - {theme['name']}")
