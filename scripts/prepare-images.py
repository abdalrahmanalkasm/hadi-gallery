#!/usr/bin/env python3
"""
prepare-images.py — turn raw artwork photographs into web-ready files.

You never resize or rename anything by hand. Put the originals in
`photos-raw/`, run this once, and it writes correctly named, correctly
sized, compressed images into `public/images/` and prints the JSON to
paste into `src/data/works.json`.

USAGE
    python3 scripts/prepare-images.py

WHAT IT EXPECTS
    photos-raw/
      sitter-late-afternoon.jpg            <- the whole work
      sitter-late-afternoon--detail-1.jpg  <- optional close-ups
      sitter-late-afternoon--detail-2.jpg
      two-chairs.jpg

    The filename before the first `--` becomes the work's slug, which
    becomes its URL. Use lowercase words joined by single hyphens. No
    spaces, no Arabic, no capitals, no accents — those break URLs.

WHAT IT DOES
    - converts anything (HEIC, PNG, TIFF, RAW export) to JPEG
    - rotates by EXIF so phone photos are not sideways
    - resizes: 2000px long edge for full works, 1600px for details
    - strips GPS and camera metadata (your home address is in there)
    - compresses to roughly 200-400 KB
    - never touches the originals

REQUIREMENTS
    pip install pillow
"""

import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "photos-raw"
OUT = ROOT / "public" / "images"

LONG_EDGE_WORK = 2000
LONG_EDGE_DETAIL = 1600
QUALITY = 84
MIN_QUALITY = 62
TARGET_KB = 420
VALID = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic", ".bmp"}


def slug_ok(name: str) -> bool:
    return all(c.isalnum() and c.isascii() or c == "-" for c in name) and name.islower()


def process(src: Path, dest: Path, long_edge: int) -> int:
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)      # honour phone rotation
    im = im.convert("RGB")                # drop alpha, CMYK, 16-bit
    if max(im.size) > long_edge:
        scale = long_edge / max(im.size)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)

    # Step quality down until the file is a reasonable size on a phone
    # connection. Saving a fresh image also drops EXIF, including GPS.
    quality = QUALITY
    while True:
        im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)
        size = dest.stat().st_size
        if size <= TARGET_KB * 1024 or quality <= MIN_QUALITY:
            return size
        quality -= 6


def main() -> None:
    if not RAW.exists():
        RAW.mkdir(parents=True)
        sys.exit(f"Created {RAW}\nPut your photographs in there and run this again.")

    OUT.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in RAW.iterdir() if p.suffix.lower() in VALID)
    if not files:
        sys.exit(f"No images found in {RAW}")

    works: dict[str, dict] = {}
    warnings: list[str] = []

    for src in files:
        stem = src.stem
        if "--detail" in stem:
            slug, tail = stem.split("--detail", 1)
            kind = "detail"
            n = tail.strip("-") or str(len(works.get(slug, {}).get("details", [])) + 1)
        else:
            slug, kind, n = stem, "work", ""

        if not slug_ok(slug):
            warnings.append(
                f"{src.name}: '{slug}' is not a safe slug. Use lowercase ASCII "
                f"words joined by hyphens, e.g. 'two-chairs'."
            )
            continue

        entry = works.setdefault(slug, {"image": None, "details": []})

        if kind == "work":
            dest = OUT / f"{slug}.jpg"
            size = process(src, dest, LONG_EDGE_WORK)
            entry["image"] = dest.name
        else:
            dest = OUT / f"{slug}-d{n}.jpg"
            size = process(src, dest, LONG_EDGE_DETAIL)
            entry["details"].append(dest.name)

        print(f"  {src.name:<44} -> {dest.name:<34} {size // 1024:>5} KB")

    for slug, e in works.items():
        e["details"].sort()
        if e["image"] is None:
            warnings.append(
                f"'{slug}' has detail photos but no main image. Add {slug}.jpg"
            )

    print(f"\nProcessed {len(files)} file(s) into {len(works)} work(s).")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ! {w}")

    print("\n" + "=" * 66)
    print("Paste these into the 'works' array in src/data/works.json,")
    print("then fill in title, year, section, medium, code, dimensions, status.")
    print("=" * 66 + "\n")

    stubs = []
    for slug, e in works.items():
        if not e["image"]:
            continue
        stubs.append({
            "slug": slug,
            "cat": "",
            "title": slug.replace("-", " ").title(),
            "year": 2026,
            "section": "paintings",
            "medium": "Oil on canvas",
            "code": "OIL/CNV",
            "dimensions": "100 × 80 cm",
            "status": "available",
            "image": e["image"],
            "details": e["details"],
            "note": "",
        })
    print(json.dumps(stubs, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
