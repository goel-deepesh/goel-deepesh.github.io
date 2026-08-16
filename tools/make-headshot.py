#!/usr/bin/env python3
"""Crop a source photo into the square headshot used in the hero.

    python3 tools/make-headshot.py photo.jpg --cx 883 --cy 600 --size 900
    python3 tools/make-headshot.py photo.jpg --preview   # 3x3 contact sheet

Coordinates are in pixels of the source image, measured from the top-left.
Smaller --size zooms in. Writes headshot.jpg, headshot.webp and og-image.jpg.
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")


def crop_square(im, cx, cy, size):
    """Crop a square of `size` centred on (cx, cy), clamped to the image."""
    half = size // 2
    left = max(0, min(cx - half, im.width - size))
    top = max(0, min(cy - half, im.height - size))
    size = min(size, im.width, im.height)
    return im.crop((left, top, left + size, top + size))


def preview(im, cx, cy, size, path):
    tiles, opts = [], []
    for dy in (-0.12, 0, 0.12):
        for zoom in (0.8, 1.0, 1.25):
            s = int(size * zoom)
            y = int(cy + size * dy)
            opts.append((cx, y, s))
    sheet = Image.new("RGB", (3 * 300, 3 * 322), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (x, y, s) in enumerate(opts):
        tile = crop_square(im, x, y, s).resize((300, 300), Image.LANCZOS)
        px, py = (i % 3) * 300, (i // 3) * 322
        sheet.paste(tile, (px, py))
        draw.text((px + 6, py + 304), f"--cx {x} --cy {y} --size {s}", fill="black")
    sheet.save(path, quality=92)
    print(f"Wrote {path}")
    print("Pick a tile, then re-run with the numbers printed beneath it.")


def main():
    p = argparse.ArgumentParser(description="Crop a photo into the site headshot.")
    p.add_argument("photo", help="path to the source image")
    p.add_argument("--cx", type=int, help="horizontal centre of the crop, in source pixels")
    p.add_argument("--cy", type=int, help="vertical centre of the crop, in source pixels")
    p.add_argument("--size", type=int, help="crop width/height in source pixels; smaller zooms in")
    p.add_argument("--preview", action="store_true", help="write a 3x3 contact sheet instead of the final files")
    p.add_argument("--out", default=ASSETS, help="output directory (default: site/assets)")
    a = p.parse_args()

    im = Image.open(a.photo).convert("RGB")

    # Sensible default: centred horizontally, upper third vertically, which is
    # roughly where a face sits in a standing portrait.
    size = a.size or int(min(im.width, im.height) * 0.5)
    cx = a.cx if a.cx is not None else im.width // 2
    cy = a.cy if a.cy is not None else int(im.height * 0.28)

    if a.preview:
        preview(im, cx, cy, size, os.path.join(a.out, "_preview.jpg"))
        return

    os.makedirs(a.out, exist_ok=True)
    sq = crop_square(im, cx, cy, size)

    big = sq.resize((800, 800), Image.LANCZOS)
    big.save(os.path.join(a.out, "headshot.jpg"), quality=88, optimize=True, progressive=True)
    big.save(os.path.join(a.out, "headshot.webp"), quality=85, method=6)

    card = Image.new("RGB", (1200, 630), (16, 18, 22))
    card.paste(sq.resize((630, 630), Image.LANCZOS), (500, 0))
    card.save(os.path.join(a.out, "og-image.jpg"), quality=88, optimize=True)

    print(f"Wrote headshot.jpg, headshot.webp and og-image.jpg to {a.out}")
    print(f"Crop used: --cx {cx} --cy {cy} --size {size}")


if __name__ == "__main__":
    main()
