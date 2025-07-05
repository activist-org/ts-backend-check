# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from pathlib import Path

from ts_backend_check.checker import TypeChecker


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

    ROOT_DIR = Path(__file__).cwd()
    parser = argparse.ArgumentParser(
        prog="ts-backend-check",
        description="Checks the types in TypeScript files against the corresponding backend models.",
        epilog="Visit the codebase at https://github.com/activist-org/ts-backend-check to learn more!",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60),
    )

    parser._actions[0].help = "Show this help message and exit."

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

    # MARK: Setup CLI

    args = parser.parse_args()
    backend_model_file_path = ROOT_DIR / args.backend_model_file
    ts_file_path = ROOT_DIR / args.typescript_file

    if not backend_model_file_path.is_file():
        print(
            f"{args.backend_model_file} that should contain the backend models does not exist. Please check and try again."
        )

    elif not ts_file_path.is_file():
        print(
            f"{args.typescript_file} file that should contain the TypeScript interfaces does not exist. Please check and try again."
        )

    else:
        checker = TypeChecker(
            models_file=args.backend_model_file,
            types_file=args.typescript_file,
        )

        if missing := checker.check():
            print("Missing typescript fields found: ")
            print("\n".join(missing))

            field_or_fields = "fields" if len(missing) > 1 else "field"
            print(
                f"\nPlease fix the {len(missing)} {field_or_fields} to have the backend models synced with the typescript interfaces."
            )
            sys.exit(1)

        print("All models are synced with their corresponding TypeScript interfaces.")


if __name__ == "__main__":
    main()
