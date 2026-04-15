from __future__ import annotations

import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"


ASCII_BANNER = r"""
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗██╗      █████╗ ██████╗
██║   ██║██║   ██║██║     ████╗  ██║██║     ██╔══██╗██╔══██╗
██║   ██║██║   ██║██║     ██╔██╗ ██║██║     ███████║██████╔╝
╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║██║     ██╔══██║██╔══██╗
 ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██████╔╝
  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═════╝
"""


@dataclass(frozen=True)
class ToolCheck:
    name: str
    command: str
    required: bool
    install_hint: str


def supports_color() -> bool:
    return sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    if not supports_color():
        return text
    return f"{color}{text}{RESET}"


def clear_screen() -> None:
    if supports_color():
        print("\033[2J\033[H", end="")


def print_banner(subtitle: str = "Local adversarial lab orchestration from your terminal.") -> None:
    print(colorize(ASCII_BANNER, GREEN))
    print(colorize(subtitle, DIM))
    print()


def print_header(title: str, subtitle: str | None = None) -> None:
    width = min(max(shutil.get_terminal_size((100, 20)).columns - 4, 50), 100)
    line = "═" * width
    print(colorize(line, GREEN))
    print(colorize(f"{BOLD}{title}{RESET}" if supports_color() else title, CYAN))
    if subtitle:
        print(colorize(subtitle, DIM))
    print(colorize(line, GREEN))


def print_success(message: str) -> None:
    print(colorize(f"[OK] {message}", GREEN))


def print_info(message: str) -> None:
    print(colorize(f"[..] {message}", CYAN))


def print_warning(message: str) -> None:
    print(colorize(f"[!] {message}", YELLOW))


def print_error(message: str) -> None:
    print(colorize(f"[X] {message}", RED))


def print_kv(key: str, value: str) -> None:
    print(f"{colorize(key + ':', MAGENTA)} {value}")


def render_progress(label: str, current: int, total: int) -> None:
    width = 28
    progress = 0 if total <= 0 else current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(progress * 100)
    print(f"\r{colorize(label, CYAN)} [{colorize(bar, GREEN)}] {percent:3d}%", end="", flush=True)
    if current >= total:
        print()


def animate_progress(label: str, steps: int = 24, delay: float = 0.03) -> None:
    for current in range(1, steps + 1):
        render_progress(label, current, steps)
        time.sleep(delay)


def confirm(prompt: str, default: bool = False) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{colorize(prompt, YELLOW)} {suffix} ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes", "s", "si"}


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def run_with_spinner(label: str, command: list[str]) -> subprocess.CompletedProcess[str]:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    stop_event = threading.Event()
    result_holder: dict[str, subprocess.CompletedProcess[str]] = {}

    def worker() -> None:
        result_holder["result"] = subprocess.run(command, text=True, capture_output=True)
        stop_event.set()

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    index = 0
    while not stop_event.is_set():
        frame = frames[index % len(frames)] if supports_color() else "*"
        print(f"\r{colorize(frame, GREEN)} {label}", end="", flush=True)
        time.sleep(0.08)
        index += 1

    thread.join()
    print("\r" + " " * (len(label) + 8) + "\r", end="")
    return result_holder["result"]
