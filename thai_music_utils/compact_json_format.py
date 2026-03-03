"""
compact_json_format.py
──────────────────────
Reformats Thai music JSON files to the compact per-bar style:
  - One bar per line
  - นำ/ตาม dict items stay inline
  - Idempotent: safe to run on already-compact files

Usage (single file):
    python3 thai_music_utils/compact_json_format.py --file path/to/song.json

Usage (whole motif folder):
    python3 thai_music_utils/compact_json_format.py --motif ลาว

Usage (all songs):
    python3 thai_music_utils/compact_json_format.py --all
"""

import json
import argparse
from pathlib import Path


# ── core formatter ────────────────────────────────────────────────────────────

def compact_item(item):
    if isinstance(item, str):
        return json.dumps(item, ensure_ascii=False)
    elif isinstance(item, dict):
        parts = []
        for k, v in item.items():
            vals = ", ".join(json.dumps(s, ensure_ascii=False) for s in v)
            parts.append('"' + k + '": [' + vals + ']')
        return "{" + ", ".join(parts) + "}"
    else:
        return json.dumps(item, ensure_ascii=False)


def compact_bar(bar):
    items = ", ".join(compact_item(x) for x in bar)
    return "[ " + items + " ]"


def reformat_file(path: Path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    lines.append("{")
    lines.append('  "title": ' + json.dumps(data["title"], ensure_ascii=False) + ',')
    lines.append('  "sections": [')

    for si, section in enumerate(data["sections"]):
        lines.append('    {')
        lines.append('      "name": ' + json.dumps(section["name"], ensure_ascii=False) + ',')
        lines.append('      "bars": [')
        bars = section["bars"]
        for bi, bar in enumerate(bars):
            comma = "," if bi < len(bars) - 1 else ""
            lines.append('        ' + compact_bar(bar) + comma)
        lines.append('      ]')
        section_comma = "," if si < len(data["sections"]) - 1 else ""
        lines.append('    }' + section_comma)

    lines.append('  ]')
    lines.append('}')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Compact Thai music JSON files to per-bar format.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file",  help="Path to a single JSON file")
    group.add_argument("--motif", help="Motif folder name, e.g. ลาว")
    group.add_argument("--all",   action="store_true", help="All motif folders under songs/")
    args = parser.parse_args()

    # resolve songs root relative to this file's location
    songs_root = Path(__file__).parent.parent / "thai_music_data" / "songs"

    targets = []

    if args.file:
        targets = [Path(args.file)]
    elif args.motif:
        targets = sorted((songs_root / args.motif).rglob("*.json"))
    elif args.all:
        targets = sorted(songs_root.rglob("*.json"))

    # skip meta.json files — only process song JSONs inside json/ folders
    targets = [p for p in targets if p.parent.name == "json"]

    print(f"Found {len(targets)} JSON file(s) to reformat.\n")
    for p in targets:
        reformat_file(p)
        print(f"  ✓  {p.relative_to(songs_root)}")

    print(f"\nDone — {len(targets)} file(s) reformatted.")


if __name__ == "__main__":
    main()
