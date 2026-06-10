#!/usr/bin/env python3
"""
update-index.py — Orbital Index auto-updater
=============================================
Scans the repo root for subfolders containing index.html and regenerates
nav-data.js so the main index page stays current automatically.

Usage (run from repo root):
    python3 scripts/update-index.py

Options:
    --dry-run    Print the generated nav-data.js without writing it
    --root DIR   Treat DIR as the repo root (default: parent of this script)

Section detection:
    Folders are grouped into sections based on their top-level parent directory.
    Known section names: demos, stories, explanations, experiments, devlogs
    Unknown folders land in "other".

Metadata extraction:
    The script reads each index.html and tries to extract:
      - <title> tag        → item title
      - <meta name="description"> → item desc
      - <meta name="tag">         → item tag  (custom, optional)
      - <meta name="featured">    → featured flag (optional, value: "true")
    Falls back to folder name / empty string if tags are missing.
"""

import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────

KNOWN_SECTIONS = {
    "demos":        "Demos",
    "stories":      "Stories",
    "explanations": "Explanations",
    "experiments":  "Experiments",
    "devlogs":      "Devlogs",
}

# Directories to always skip
SKIP_DIRS = {
    ".git", ".github", "scripts", "node_modules",
    "__pycache__", ".vscode", ".idea", "assets", "css", "js",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def read_meta(html_path: Path) -> dict:
    """Extract title, desc, tag, featured from an HTML file."""
    try:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}

    meta = {}

    # <title>
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if m:
        meta["title"] = re.sub(r"\s+", " ", m.group(1)).strip()

    # <meta name="description" content="...">
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
                  text, re.IGNORECASE)
    if m:
        meta["desc"] = m.group(1).strip()

    # <meta name="tag" content="...">
    m = re.search(r'<meta\s+name=["\']tag["\']\s+content=["\'](.*?)["\']',
                  text, re.IGNORECASE)
    if m:
        meta["tag"] = m.group(1).strip()

    # <meta name="featured" content="true">
    m = re.search(r'<meta\s+name=["\']featured["\']\s+content=["\'](.*?)["\']',
                  text, re.IGNORECASE)
    if m:
        meta["featured"] = m.group(1).strip().lower() == "true"

    return meta


def folder_to_title(folder_name: str) -> str:
    """Convert a folder name like 'my-cool-game' to 'My Cool Game'."""
    return folder_name.replace("-", " ").replace("_", " ").title()


def get_mtime(path: Path) -> str:
    """ISO date string of a file's last modification time."""
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


# ── Scanner ───────────────────────────────────────────────────────────────────

def scan(root: Path) -> dict:
    """
    Walk root, find index.html files in subdirectories,
    group them into sections, return structured data.
    """
    sections: dict[str, list] = {}

    for section_dir in sorted(root.iterdir()):
        if not section_dir.is_dir():
            continue
        if section_dir.name.startswith(".") or section_dir.name in SKIP_DIRS:
            continue

        section_key = section_dir.name.lower()
        section_label = KNOWN_SECTIONS.get(section_key,
                        folder_to_title(section_dir.name))

        items = []
        for project_dir in sorted(section_dir.iterdir()):
            if not project_dir.is_dir():
                continue
            if project_dir.name.startswith(".") or project_dir.name in SKIP_DIRS:
                continue

            html = project_dir / "index.html"
            if not html.exists():
                continue

            meta = read_meta(html)
            rel_path = html.relative_to(root).as_posix()

            item = {
                "title":    meta.get("title") or folder_to_title(project_dir.name),
                "path":     rel_path,
                "desc":     meta.get("desc", ""),
                "tag":      meta.get("tag", ""),
                "featured": meta.get("featured", False),
                "updated":  get_mtime(html),
            }
            # Remove empty optional fields to keep the output clean
            if not item["tag"]:     del item["tag"]
            if not item["desc"]:    del item["desc"]
            if not item["featured"]: del item["featured"]

            items.append(item)

        if items:
            sections[section_key] = {
                "label": section_label,
                "items": items,
            }

    return sections


# ── Renderer ──────────────────────────────────────────────────────────────────

def render_js(sections: dict, generated: str) -> str:
    """Render the NAV_DATA JS file as a string."""

    lines = []
    lines.append("/**")
    lines.append(" * nav-data.js — AUTO-GENERATED by scripts/update-index.py")
    lines.append(f" * Generated: {generated}")
    lines.append(" * DO NOT edit by hand — run the script again to update.")
    lines.append(" * To add custom descriptions/tags, edit the source index.html")
    lines.append(' * using <meta name="description" content="..."> etc.')
    lines.append(" */")
    lines.append("")
    lines.append("const NAV_DATA = {")
    lines.append("")
    lines.append(f'  meta: {{')
    lines.append(f'    title:       "Orbital Index",')
    lines.append(f'    description: "Games, stories, and demos",')
    lines.append(f'    generated:   "{generated}",')
    lines.append(f'  }},')
    lines.append("")
    lines.append("  sections: {")
    lines.append("")

    for i, (key, section) in enumerate(sections.items()):
        lines.append(f'    {key}: {{')
        lines.append(f'      label: "{section["label"]}",')
        lines.append(f'      items: [')
        for item in section["items"]:
            lines.append("        {")
            lines.append(f'          title:    {json.dumps(item["title"])},')
            lines.append(f'          path:     {json.dumps(item["path"])},')
            if "desc" in item:
                lines.append(f'          desc:     {json.dumps(item["desc"])},')
            if "tag" in item:
                lines.append(f'          tag:      {json.dumps(item["tag"])},')
            if item.get("featured"):
                lines.append(f'          featured: true,')
            lines.append(f'          updated:  {json.dumps(item["updated"])},')
            lines.append("        },")
        lines.append("      ],")
        lines.append("    },")
        lines.append("")

    lines.append("  },")
    lines.append("")
    lines.append("};")
    lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Regenerate nav-data.js for Orbital Index")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print output without writing file")
    parser.add_argument("--root", type=Path, default=None,
                        help="Repo root directory (default: parent of scripts/)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = args.root or script_dir.parent

    print(f"[orbital] Scanning: {root}")

    sections = scan(root)
    total = sum(len(s["items"]) for s in sections.values())
    print(f"[orbital] Found {total} projects across {len(sections)} sections")

    generated = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    output = render_js(sections, generated)

    if args.dry_run:
        print("\n" + "─" * 60)
        print(output)
        return

    out_path = root / "nav-data.js"
    out_path.write_text(output, encoding="utf-8")
    print(f"[orbital] Written → {out_path}")
    print("[orbital] Done. Reload index.html to see changes.")


if __name__ == "__main__":
    main()
