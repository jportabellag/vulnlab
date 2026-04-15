from __future__ import annotations

from pathlib import Path

from vulnlab.console import print_header, print_warning
from vulnlab.paths import get_asset_root


BASE_DIR = get_asset_root()


def walkthrough_path(slug: str) -> Path:
    return BASE_DIR / "docs" / "solutions" / f"{slug}.md"


def print_walkthrough(slug: str) -> None:
    path = walkthrough_path(slug)
    print_header(f"Walkthrough: {slug}")
    if not path.exists():
        print_warning("No walkthrough available for this lab yet.")
        return
    print(path.read_text())
