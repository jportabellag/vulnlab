from __future__ import annotations

import os
import sys
from pathlib import Path


def _candidate_roots() -> list[Path]:
    candidates: list[Path] = []

    env_home = os.environ.get("VULNLAB_HOME")
    if env_home:
        candidates.append(Path(env_home).expanduser())

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        candidates.append(Path(xdg_data_home).expanduser() / "vulnlab")

    candidates.append(Path.home() / ".local" / "share" / "vulnlab")

    executable = Path(sys.executable).resolve()
    candidates.append(executable.parent.parent / "share" / "vulnlab")

    package_root = Path(__file__).resolve().parent.parent
    candidates.append(package_root)

    return candidates


def get_asset_root() -> Path:
    for candidate in _candidate_roots():
        if (candidate / "docker").exists() and (candidate / "docs").exists():
            return candidate

    return Path(__file__).resolve().parent.parent
