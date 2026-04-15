from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path

from vulnlab.console import (
    ToolCheck,
    animate_progress,
    command_exists,
    confirm,
    print_error,
    print_header,
    print_info,
    print_kv,
    print_success,
    print_warning,
    run_with_spinner,
)


TOOLING = [
    ToolCheck("Docker", "docker", True, "Docker Desktop or a compatible Docker engine"),
    ToolCheck("Git", "git", True, "git"),
    ToolCheck("Nmap", "nmap", False, "nmap"),
    ToolCheck("Redis CLI", "redis-cli", False, "redis-cli / redis-tools"),
]

STATE_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "vulnlab"
STATE_FILE = STATE_DIR / "state.json"


def run_doctor() -> int:
    print_header("Environment Doctor", "Checking external dependencies and local prerequisites.")
    missing_required = False

    for tool in TOOLING:
        if command_exists(tool.command):
            print_success(f"{tool.name} detected")
        else:
            if tool.required:
                missing_required = True
                print_error(f"{tool.name} missing")
            else:
                print_warning(f"{tool.name} missing")
            print_kv("Install", tool.install_hint)

    return 1 if missing_required else 0


def _load_state() -> dict[str, bool]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _save_state(state: dict[str, bool]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))


def _missing_tools() -> tuple[list[ToolCheck], list[ToolCheck]]:
    required_missing: list[ToolCheck] = []
    optional_missing: list[ToolCheck] = []
    for tool in TOOLING:
        if command_exists(tool.command):
            continue
        if tool.required:
            required_missing.append(tool)
        else:
            optional_missing.append(tool)
    return required_missing, optional_missing


def _install_command(tool: ToolCheck) -> list[str] | None:
    system = platform.system().lower()
    if tool.command == "git":
        if command_exists("brew"):
            return ["brew", "install", "git"]
        if system == "linux" and command_exists("apt-get"):
            return ["sudo", "apt-get", "install", "-y", "git"]
    if tool.command == "docker":
        if command_exists("brew"):
            return ["brew", "install", "--cask", "docker"]
    return None


def run_setup() -> int:
    print_header("Setup Wizard", "Optional bootstrap for external dependencies.")
    animate_progress("Preparing installer profile", steps=16, delay=0.02)

    for tool in TOOLING:
        if command_exists(tool.command):
            print_success(f"{tool.name} already installed")
            continue

        print_warning(f"{tool.name} is not installed")
        print_kv("Hint", tool.install_hint)

        command = _install_command(tool)
        if not command:
            print_warning(f"No automatic installer configured for {tool.name} on this system")
            continue

        if not confirm(f"Install {tool.name} using: {' '.join(command)}?", default=False):
            print_info(f"Skipped installation of {tool.name}")
            continue

        animate_progress(f"Scheduling {tool.name} installation", steps=20, delay=0.02)
        result = run_with_spinner(f"Installing {tool.name}", command)
        if result.returncode == 0:
            print_success(f"{tool.name} installed")
        else:
            print_error(f"{tool.name} installation failed")
            if result.stderr.strip():
                print(result.stderr.strip())

    print()
    return run_doctor()


def run_first_launch_bootstrap() -> int:
    state = _load_state()
    if state.get("bootstrap_complete"):
        return 0

    required_missing, optional_missing = _missing_tools()
    if not required_missing and not optional_missing:
        state["bootstrap_complete"] = True
        _save_state(state)
        return 0

    print_header("First Launch Setup", "Reviewing system dependencies before opening the terminal UI.")

    if required_missing:
        print_warning("Required dependencies are missing.")
        for tool in required_missing:
            print_kv(tool.name, tool.install_hint)
    else:
        print_success("Required dependencies detected")

    if optional_missing:
        print_info("Optional tooling available for lab work can also be installed.")
        for tool in optional_missing:
            print_kv(tool.name, tool.install_hint)

    if confirm("Run guided dependency setup now?", default=True):
        run_setup()
    else:
        print_info("Skipping guided dependency setup")

    state["bootstrap_complete"] = True
    _save_state(state)
    return 0
