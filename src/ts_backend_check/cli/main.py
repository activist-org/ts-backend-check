# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path

from rich import print as rprint
from rich.text import Text

from ts_backend_check.checker import TypeChecker
from ts_backend_check.cli.check_blank import check_blank
from ts_backend_check.cli.config import create_config
from ts_backend_check.cli.upgrade import upgrade_cli
from ts_backend_check.cli.version import get_version_message

ROOT_DIR = Path.cwd()


def main() -> None:
    """
    The main check function to compare a the methods within a backend model to a corresponding TypeScript file.

    Notes
    -----
    The available command line arguments are:
    - --backend-model-file (-bmf): Path to the backend model file (e.g. Python class)
    - --typescript-file (-tsf): Path to the TypeScript interface/type file

    Examples
    --------
    >>> ts-backend-check -bmf <backend-model-file> -tsf <typescript-file>
    """
    # MARK: CLI Base

    parser = ArgumentParser(
        prog="ts-backend-check",
        description="Checks the types in TypeScript files against the corresponding backend models.",
        epilog="Visit the codebase at https://github.com/activist-org/ts-backend-check to learn more!",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60),
    )

    parser._actions[0].help = "Show this help message and exit."

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{get_version_message()}",
        help="Show the version of the ts-backend-check CLI.",
    )

    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade the ts-backend-check CLI to the latest version.",
    )

    parser.add_argument(
        "-bmf",
        "--backend-model-file",
        help="Path to the backend model file (e.g. Python class).",
    )

    parser.add_argument(
        "-tsf",
        "--typescript-file",
        help="Path to the TypeScript interface/type file.",
    )

    parser.add_argument(
        "-c",
        "--configure",
        action="store_true",
        help="Configure a YAML file to simplify your checks.",
    )

    parser.add_argument(
        "-cb",
        "--check-blank",
        help="Check for fields marked blank=True within Django models.",
    )

    # MARK: Setup CLI

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.upgrade:
        upgrade_cli()
        return

    if args.configure:
        create_config()
        return

    if args.check_blank:
        check_blank(args.check_blank)
        return

    # MARK: Run Check

    backend_model_file_path = ROOT_DIR / args.backend_model_file
    ts_file_path = ROOT_DIR / args.typescript_file

    if not backend_model_file_path.is_file():
        rprint(
            f"[red]{args.backend_model_file} that should contain the backend models does not exist. Please check and try again.[/red]"
        )

    elif not ts_file_path.is_file():
        rprint(
            f"[red]{args.typescript_file} file that should contain the TypeScript types does not exist. Please check and try again.[/red]"
        )

    else:
        checker = TypeChecker(
            models_file=args.backend_model_file,
            types_file=args.typescript_file,
        )

        if missing := checker.check():
            rprint(
                "\n[red]❌ ts-backend-check error: There are inconsistencies between the provided backend models and TypeScript interfaces. Please see the output below for details.[/red]"
            )

            # Print each error message in red.
            for msg in missing:
                rprint(Text.from_markup(f"[red]{msg}[/red]"))

            field_or_fields = "fields" if len(missing) > 1 else "field"
            rprint(
                f"[red]\nPlease fix the {len(missing)} {field_or_fields} above to have the backend models of {args.backend_model_file} synced with the typescript interfaces of {(args.typescript_file)}.[/red]"
            )
            sys.exit(1)

        rprint(
            "[green]✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided files.[/green]"
        )


if __name__ == "__main__":
    main()
