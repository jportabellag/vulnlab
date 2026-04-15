from __future__ import annotations

import sys

from vulnlab.console import clear_screen, print_banner, print_header
from vulnlab.labs import LABS, LabDefinition
from vulnlab.manager import (
    create_lab,
    print_lab_info,
    print_lab_status,
    print_labs,
    print_logs,
    remove_lab,
    reset_lab,
    stop_lab,
)
from vulnlab.docs import print_walkthrough
from vulnlab.verify import run_verification


def _print_banner() -> None:
    print_banner("Terminal-first breach lab runner with guided workflows.")


def _choose(prompt: str, options: list[str]) -> int:
    while True:
        print_header(prompt)
        for index, option in enumerate(options, start=1):
            print(f"  {index}. {option}")

        selected = input("\nSelect an option: ").strip()
        if selected.isdigit():
            value = int(selected)
            if 1 <= value <= len(options):
                print()
                return value - 1

        print("Invalid selection.\n")


def _choose_lab() -> LabDefinition | None:
    ordered = list(LABS.values())
    options = [f"{lab.slug} | {lab.title} | {lab.difficulty}" for lab in ordered]
    options.append("Back")
    selected = _choose("Available Labs", options)
    if selected == len(ordered):
        return None
    return ordered[selected]


def _run_lab_action(action: str, lab: LabDefinition) -> None:
    if action == "create":
        create_lab(lab)
    elif action == "inspect":
        print_lab_info(lab)
        print()
        print_lab_status(lab)
    elif action == "stop":
        stop_lab(lab)
    elif action == "remove":
        remove_lab(lab)
    elif action == "reset":
        reset_lab(lab)
    elif action == "info":
        print_lab_info(lab)
    elif action == "status":
        print_lab_status(lab)
    elif action == "logs":
        tail = input("Log tail [50]: ").strip() or "50"
        print_logs(lab, tail=int(tail))
    elif action == "walkthrough":
        print_walkthrough(lab.slug)


def _pause() -> None:
    input("\nPress Enter to continue...")


def _print_main_screen() -> list[str]:
    print_header("Main Menu", "Single-screen command board grouped by function.")

    action_keys: list[str] = []
    current = 1
    sections = [
        (
            "Lab Registry",
            [
                ("registry", "List available labs"),
            ],
        ),
        (
            "Lab Operations",
            [
                ("create", "Create lab"),
                ("inspect", "Inspect lab"),
                ("logs", "Show logs"),
                ("reset", "Reset lab"),
                ("stop", "Stop lab"),
                ("remove", "Remove lab"),
            ],
        ),
        (
            "Learning",
            [
                ("walkthrough", "Show walkthrough"),
            ],
        ),
        (
            "System Tools",
            [
                ("verify", "Quick repository verification"),
                ("verify_docker", "Docker verification for a lab"),
                ("doctor", "Environment doctor"),
                ("setup", "Dependency setup"),
            ],
        ),
        (
            "Session",
            [
                ("exit", "Exit"),
            ],
        ),
    ]

    for section_title, entries in sections:
        print(section_title)
        print("-" * len(section_title))
        for action_key, label in entries:
            print(f"  {current}. {label}")
            action_keys.append(action_key)
            current += 1
        print()

    return action_keys


def _choose_main_action() -> str:
    action_keys = _print_main_screen()
    while True:
        selected = input("Select an option: ").strip()
        if selected.isdigit():
            index = int(selected) - 1
            if 0 <= index < len(action_keys):
                print()
                return action_keys[index]
        print("Invalid selection.\n")


def launch_menu() -> int:
    while True:
        _print_banner()
        action = _choose_main_action()

        if action == "registry":
            print_labs()
            _pause()
        elif action in {"create", "inspect", "logs", "reset", "stop", "remove", "walkthrough"}:
            lab = _choose_lab()
            if not lab:
                continue
            _run_lab_action(action, lab)
            _pause()
        elif action == "verify":
            for check in run_verification(target="all", include_docker=False):
                print(f"[+] {check}")
            _pause()
        elif action == "verify_docker":
            lab = _choose_lab()
            if not lab:
                continue
            for check in run_verification(target=lab.slug, include_docker=True):
                print(f"[+] {check}")
            _pause()
        elif action == "doctor":
            from vulnlab.setup import run_doctor

            run_doctor()
            _pause()
        elif action == "setup":
            from vulnlab.setup import run_setup

            run_setup()
            _pause()
        else:
            return 0

        clear_screen()


def should_launch_menu(argv: list[str] | None) -> bool:
    args = argv if argv is not None else sys.argv[1:]
    return (not args and sys.stdin.isatty()) or (args and args[0] == "menu")
