from __future__ import annotations

import argparse
import sys

from vulnlab import __version__
from vulnlab.console import print_error, print_success
from vulnlab.docs import print_walkthrough
from vulnlab.docker import DockerCommandError
from vulnlab.labs import LABS, get_lab
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
from vulnlab.setup import run_doctor, run_first_launch_bootstrap, run_setup
from vulnlab.ui import launch_menu, should_launch_menu
from vulnlab.verify import run_verification


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vulnlab",
        description="Terminal-first CLI for launching vulnerable local labs with Docker.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    lab_commands = ["create", "stop", "remove", "reset", "info", "status", "logs", "walkthrough"]

    for command in lab_commands:
        subparser = subparsers.add_parser(command)
        subparser.add_argument("lab", choices=sorted(LABS.keys()))
        if command == "logs":
            subparser.add_argument("--tail", type=int, default=50)

    subparsers.add_parser("list")
    subparsers.add_parser("menu")
    subparsers.add_parser("doctor")
    subparsers.add_parser("setup")
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("lab", nargs="?", choices=["all", *sorted(LABS.keys())], default="all")
    verify_parser.add_argument("--docker", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    raw_args = sys.argv[1:] if argv is None else argv
    interactive = sys.stdin.isatty()
    if interactive and not raw_args:
        run_first_launch_bootstrap()

    if should_launch_menu(argv):
        return launch_menu()

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "list":
            print_labs()
            return 0
        if args.command == "menu":
            return launch_menu()
        if args.command == "doctor":
            return run_doctor()
        if args.command == "setup":
            return run_setup()
        if args.command == "verify":
            for check in run_verification(target=args.lab, include_docker=args.docker):
                print_success(check)
            return 0

        lab = get_lab(args.lab)
        if not lab:
            print_error(f"Lab not found: {args.lab}")
            return 1

        if args.command == "create":
            create_lab(lab)
        elif args.command == "stop":
            stop_lab(lab)
        elif args.command == "remove":
            remove_lab(lab)
        elif args.command == "reset":
            reset_lab(lab)
        elif args.command == "info":
            print_lab_info(lab)
        elif args.command == "status":
            print_lab_status(lab)
        elif args.command == "logs":
            print_logs(lab, tail=args.tail)
        elif args.command == "walkthrough":
            print_walkthrough(lab.slug)
        else:
            parser.print_help()
            return 1

        return 0
    except DockerCommandError as exc:
        print_error(str(exc))
        return 1
    except KeyboardInterrupt:
        print_error("Operation cancelled")
        return 130


if __name__ == "__main__":
    sys.exit(main())
