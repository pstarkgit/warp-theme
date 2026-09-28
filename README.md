# Copper Glow for Warp

A dark terminal theme with a visible copper and amber nebula glow behind the text, a molten copper UI accent, and a SeaShells-inspired teal counterpoint.

## Install

Copy both files into Warp's themes directory:

```sh
mkdir -p ~/.warp/themes
cp copper-glow.yaml copper-glow.jpg ~/.warp/themes/
```

Select **Copper Glow** in **Settings → Appearance → Themes**. The wallpaper stays darkest through the center for readable command output and glows along the left and lower-right edges.

## Afterlight collection

Open [the Afterlight gallery](afterlight/index.html) to preview six more glow themes:

- **Afterlight - Aurora Tide** — teal, ice blue, and violet
- **Afterlight - Aurora Prism** — ice blue, lavender, and rose
- **Afterlight - Aurora Canopy** — jade, lime, and soft gold
- **Afterlight - Orchid Haze** — violet and blush
- **Afterlight - Solar Ember** — copper, amber, and rose
- **Afterlight - Ember Focus** — near-black with a restrained copper accent

Each theme has an `afterlight-*.yaml` file and matching `afterlight-*.jpg` wallpaper in `afterlight/`. Copy all six pairs into `~/.warp/themes/` to keep them together in Warp's theme list, then select a theme in Warp:

```sh
cp afterlight/afterlight-*.yaml afterlight/afterlight-*.jpg ~/.warp/themes/
```

The gallery uses PNG previews. On macOS, run `python3 afterlight/generate.py` to regenerate the YAML, PNG, and Warp-compatible JPEG files using the built-in `sips` command.

## License

MIT. See [LICENSE](LICENSE).
