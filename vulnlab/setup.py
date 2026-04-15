from __future__ import annotations

import platform
from dataclasses import dataclass

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
    ToolCheck("Docker", "docker", True, "Docker Desktop o motor Docker compatible"),
    ToolCheck("Git", "git", True, "git"),
]


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
