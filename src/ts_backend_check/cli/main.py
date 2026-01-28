# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path

import yaml
from rich import print as rprint
from rich.text import Text

from ts_backend_check.checker import TypeChecker
from ts_backend_check.cli.generate_config_file import generate_config_file
from ts_backend_check.cli.generate_test_project import generate_test_project
from ts_backend_check.cli.upgrade import upgrade_cli
from ts_backend_check.cli.version import get_version_message

# MARK: Base Paths

CWD_PATH = Path.cwd()


def get_config_file_path() -> Path:
    """
    Get the path to the ts-backend-check configuration file.

    Checks for both .yaml and .yml extensions, preferring .yaml if both exist.

    Returns
    -------
    Path
        The path to the configuration file (.yaml or .yml).
    """
    yaml_path = CWD_PATH / ".ts-backend-check.yaml"
    yml_path = CWD_PATH / ".ts-backend-check.yml"

    # Prefer .yaml if it exists, otherwise check for .yml.
    if yaml_path.is_file():
        return yaml_path

    elif yml_path.is_file():
        return yml_path

    else:
        # Default to .yaml for new files.
        return yaml_path


YAML_CONFIG_FILE_PATH = get_config_file_path()


# MARK: CLI Vars

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    generate_config_file()

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    print(
        "No configuration file. Please generate a configuration file (.ts-backend-check.yaml or .ts-backend-check.yml) with ts-backend-check -gcf."
    )
    exit(1)

with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)


def check_files_and_print_results(
    model: str,
    backend_model_file_path: Path,
    ts_interface_file_path: Path,
    check_blank: bool = False,
) -> bool:
    """
    Check the provided files for the given model and print the results.

    Parameters
    ----------
    model : str
        The model in the .ts-backend-check.yaml configuration file to check models and interfaces for.

    backend_model_file_path : Path
        The path to the backend models as defined in the .ts-backend-check.yaml configuration file .

    ts_interface_file_path : Path
        The path to the TypeScript interfaces as defined in the .ts-backend-check.yaml configuration file .

    check_blank : bool
        Whether to also check that fields marked blank=True within Django models are optional in the TypeScript interfaces.

    Returns
    -------
    bool
        Whether the checks passed (True) or not (False).
    """
    if not backend_model_file_path.is_file():
        rprint(
            f"[red]❌ {backend_model_file_path} that should contain the '{model}' backend models does not exist. Please check the ts-backend-check configuration file and try again.[/red]"
        )

    elif not ts_interface_file_path.is_file():
        rprint(
            f"[red]❌ {ts_interface_file_path} that should contain the '{model}' TypeScript types does not exist. Please check the ts-backend-check configuration file and try again.[/red]"
        )

    checker = TypeChecker(
        models_file=str(backend_model_file_path),
        types_file=str(ts_interface_file_path),
        check_blank=check_blank,
    )

    if missing := checker.check():
        rprint(
            f"\n[red]❌ ts-backend-check error: There are inconsistencies between the provided {model} backend models and TypeScript interfaces. Please see the output below for details.[/red]"
        )

        for msg in missing:
            rprint(Text.from_markup(f"[red]{msg}[/red]"))

        field_or_fields = "fields" if len(missing) > 1 else "field"
        rprint(
            f"[red]\nPlease fix the {len(missing)} {field_or_fields} above to have the backend models of {backend_model_file_path} synced with the typescript interfaces of {ts_interface_file_path}.[/red]"
        )

        return False

    else:
        rprint(
            f"[green]✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided '{model}' files.[/green]"
        )

        return True


def main() -> None:
    """
    The main check function to compare a the methods within a backend model to a corresponding TypeScript file.

    Notes
    -----
    The available command line arguments are:
    - --help (-h): Show this help message and exit.
    - --version (-v): Show the version of the ts-backend-check CLI.
    - --upgrade (-u): Upgrade the ts-backend-check CLI to the latest version.
    - --generate-config-file (-gcf): Interactively generate a configuration file for ts-backend-check.
    - --generate-test-project (-gtp): Generate project to test ts-backend-check functionalities.
    - --model (-m): The model in the .ts-backend-check.yaml configuration file to check.
    - --all (-a): Run checks of all backend models against their corresponding TypeScript interfaces.

    Examples
    --------
    >>> ts-backend-check --generate-config-file  # -gcf
    >>> ts-backend-check --model <ts-backend-check-config-file-model>  # -m
    >>> ts-backend-check --all  # -a
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
        "-gcf",
        "--generate-config-file",
        action="store_true",
        help="Interactively generate a configuration file for ts-backend-check.",
    )

    parser.add_argument(
        "-gtp",
        "--generate-test-project",
        action="store_true",
        help="Generate project to test ts-backend-check functionalities.",
    )

    parser.add_argument(
        "-m",
        "--model",
        help="The model in the .ts-backend-check.yaml configuration file to check.",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run checks of all backend models against their corresponding TypeScript interfaces.",
    )

    # MARK: Setup CLI

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.upgrade:
        upgrade_cli()
        return

    if args.generate_config_file:
        generate_config_file()
        return

    if args.generate_test_project:
        generate_test_project()
        return

    # MARK: Run Checks

    checks_fail = []

    if args.model:
        if not config[args.model]:
            rprint(
                f"[red]{args.model} is not an index within the .ts-backend-check.yaml configuration file. Please check the defined models and try again.[/red]"
            )
            return

        config_backend_model_file_path = Path(config[args.model]["backend_model_path"])
        config_ts_interface_file_path = Path(config[args.model]["ts_interface_path"])
        config_check_blank = config[args.model]["check_blank"]

        checks_fail.append(
            check_files_and_print_results(
                model=args.model,
                backend_model_file_path=config_backend_model_file_path,
                ts_interface_file_path=config_ts_interface_file_path,
                check_blank=config_check_blank,
            )
        )

    if args.all:
        for m in config.keys():
            config_backend_model_file_path = Path(config[m]["backend_model_path"])
            config_ts_interface_file_path = Path(config[m]["ts_interface_path"])
            config_check_blank = config[args.model]["check_blank"]

            checks_fail.append(
                check_files_and_print_results(
                    model=m,
                    backend_model_file_path=config_backend_model_file_path,
                    ts_interface_file_path=config_ts_interface_file_path,
                    check_blank=config_check_blank,
                )
            )

    if (args.model or args.all) and not any(checks_fail):
        sys.exit(1)

    elif args.model or args.all:
        return

    else:
        parser.print_help()
