# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from pathlib import Path

from ts_backend_check.checker import TypeChecker

ROOT_DIR = Path(__file__).cwd()
parser = argparse.ArgumentParser(
    prog="ts-backend-checker",
    description="Checks the types in TypeScript files against the corresponding backend models.",
)

parser.add_argument("-bmf", "--backend-model-file")
parser.add_argument("-tsf", "--typescript-file")


def main() -> None:
    """
    The main check function to compare a the methods within a backend model to a corresponding TypeScript file.
    """
    args = parser.parse_args()
    args_dict = vars(args)
    backend_model_file_path = ROOT_DIR / f"{args_dict['backend_model_file']}"
    ts_file_path = ROOT_DIR / f"{args_dict['typescript_file']}"

    if not backend_model_file_path.is_file():
        print("File containing the Django Model does not exist. Please check again.")

    elif not ts_file_path.is_file():
        print(
            "File containing the TypeScript Interface does not exist. Please check again."
        )

    else:
        checker = TypeChecker(
            models_file=args_dict["backend_model_file"],
            types_file=args_dict["typescript_file"],
        )

        if missing := checker.check():
            print("Missing typescript fields found: ")
            print("\n".join(missing))
            print(
                f"\nPlease fix the {len(missing)} fields to have the backend models synced with the typescript models."
            )
            sys.exit(1)

        print("All models are synced perfectly.")


if __name__ == "__main__":
    main()
