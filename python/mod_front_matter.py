#!/usr/bin/env python3

"""
convert_front_matter.py

Detects Hugo PaperMod vs Astro front matter in a Markdown file,
converts PaperMod to AstroLaunch UI format, and updates/inserts
key-value pairs via CLI.

Value Created: Simplifies Hugo→Astro migrations with repeatable structure.
Audience: Developers migrating static sites between frameworks.
"""

import sys
import argparse
import frontmatter
from pathlib import Path
import re
import yaml

def detect_format(fm: dict) -> str:
    if "type" in fm or "author" in fm or "ShowReadingTime" in fm:
        return "papermod"
    elif "layout" in fm or "pageTitle" in fm or "description" in fm:
        return "astrolaunch"
    return "unknown"

def convert_to_astrolaunch(fm: dict) -> dict:
    return {
        "layout": "blog",
        "pageTitle": fm.get("title", ""),
        "description": fm.get("description", fm.get("summary", "")),
        "publishDate": str(fm.get("date", "")),
        "updatedDate": str(fm.get("lastmod", "")),
        "author": fm.get("author", ""),
        "draft": fm.get("draft", False),
        "tags": fm.get("tags", []),
    }

def update_or_insert(fm: dict, overrides: list[tuple[str, str]]) -> dict:
    for k, v in overrides:
        try:
            v_parsed = yaml.safe_load(v)
        except yaml.YAMLError:
            v_parsed = v
        fm[k] = v_parsed
    return fm

def main():
    parser = argparse.ArgumentParser(description="Convert PaperMod to AstroLaunch UI front matter.")
    parser.add_argument("filepath", type=Path, help="Markdown file to process")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE", help="Key-value pair to update/add")

    args = parser.parse_args()

    if not args.filepath.exists():
        sys.exit("File not found.")

    post = frontmatter.load(args.filepath)
    fmt = detect_format(post.metadata)
    print(f"Detected format: {fmt}")

    if fmt == "papermod":
        post.metadata = convert_to_astrolaunch(post.metadata)
        print("Converted to AstroLaunch UI front matter.")

    if args.set:
        overrides = []
        for item in args.set:
            if "=" not in item:
                sys.exit(f"Invalid format for --set: {item}")
            key, value = item.split("=", 1)
            overrides.append((key, value))
        post.metadata = update_or_insert(post.metadata, overrides)
        print("Applied overrides.")

    # Rewrite file
    with open(args.filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
        print(f"Updated: {args.filepath}")

if __name__ == "__main__":
    main()

