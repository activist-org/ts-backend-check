# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import yaml
from rich import print as rprint
from rich.text import Text

from ts_backend_check.checker import TypeChecker
from ts_backend_check.cli.generate_config_file import (
    config_file_is_valid,
    generate_config_file,
)
from ts_backend_check.cli.generate_test_project import generate_test_project
from ts_backend_check.cli.upgrade import upgrade_cli
from ts_backend_check.cli.version import get_version_message
from ts_backend_check.utils import get_config_file_path

# MARK: Base Paths


def check_files_and_print_results(
    identifier: str,
    backend_model_file_path: Path,
    ts_interface_file_paths: list[Path],
    backend_type: str,
    check_blank: bool = False,
    model_name_conversions: dict[str, list[str]] = {},
    backend_models_to_ignore: list[str] = [],
) -> bool:
    """
    Check the provided files for the given model and print the results.

    Parameters
    ----------
    identifier : str
        The model in the .ts-backend-check.yaml configuration file to check models and interfaces for.

    backend_model_file_path : Path
        The path to the backend models as defined in the .ts-backend-check.yaml configuration file.

    ts_interface_file_paths : list[Path]
        The paths to the TypeScript interfaces as defined in the .ts-backend-check.yaml configuration file.

    backend_type : str
        The backend type to check against, either 'django' or 'fastapi'.

    check_blank : bool, default=False
        Whether to also check that fields marked 'blank=True' within Django models are optional (?) in the TypeScript interfaces.

    model_name_conversions : dict[str, list[str]], default={}
        A dictionary of backend model names to their corresponding TypeScript interfaces when snake to camel case isn't valid.

    backend_models_to_ignore : list[str]
        Backend model classes to ignore, obtained from the config file.

    Returns
    -------
    bool
        Whether the checks passed (True) or not (False).
    """
    if not backend_model_file_path.is_file():
        rprint(
            f"[red]❌ The 'backend_model_file_path' argument, {backend_model_file_path}, is not a valid file. This should be a file that contains the '{identifier}' backend models. Please check the .ts-backend-check.yaml configuration file and try again.[/red]"
        )
        return False

    ts_interface_file_path_validities = [p.is_file() for p in ts_interface_file_paths]
    if invalid_ts_interface_file_paths := [
        str(p)
        for i, p in enumerate(ts_interface_file_paths)
        if not ts_interface_file_path_validities[i]
    ]:
        rprint(
            f"[red]❌ The 'ts_interface_file_paths' argument should contain paths to the '{identifier}' TypeScript types. The following paths do not lead to valid files:\n\n- {'\n- '.join(invalid_ts_interface_file_paths)}\n"
            "\nPlease check the .ts-backend-check.yaml configuration file and try again.[/red]"
        )
        return False

    # We concatenate all contents of the interface files into a single interface.
    # Note: This means that we can't report which interface file the errors are coming from.
    concatenated_types_file = ""
    for p in ts_interface_file_paths:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    checker = TypeChecker(
        models_file=str(backend_model_file_path),
        concatenated_types_file=concatenated_types_file,
        model_name_conversions=model_name_conversions,
        backend_type=backend_type,
        check_blank=check_blank,
        backend_models_to_ignore=backend_models_to_ignore,
    )

    if missing := checker.check():
        rprint(
            f"\n[red]❌ ts-backend-check error: There are inconsistencies between the provided '{identifier}' backend models and TypeScript interfaces. Please see the output below for details.[/red]"
        )

        for msg in missing:
            rprint(Text.from_markup(f"[red]{msg}[/red]"))

        error_or_errors = "errors" if len(missing) > 1 else "error"
        rprint(
            f"[red]\nPlease fix the {len(missing)} {error_or_errors} above to continue the sync of the backend models of {backend_model_file_path} and the corresponding TypeScript interfaces.[/red]"
        )

        return False

    else:
        rprint(
            f"[green]✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided '{identifier}' files.[/green]"
        )

        return True


# MARK: Config Checks


def extract_identifier_config(
    identifier_config: dict, backend_type_filter: str
) -> dict[str, Any]:
    """
    Extract and normalize config fields with defaults.

    Parameters
    ----------
    identifier_config : dict
        A dictionary of configuration parameters, with some being unset.

    backend_type_filter : str
        The backend type to check against, either 'django' or 'fastapi'.

    Returns
    -------
    dict[str,Any]
        A dict of configuration parameters to pass to checks with defaults set.
    """
    return {
        "backend_model_file_path": Path(identifier_config["backend_model_path"]),
        "ts_interface_file_paths": [
            Path(p) for p in identifier_config["ts_interface_paths"]
        ],
        # We default to Django if the backend type is not specified in the config file.
        "backend_type": identifier_config.get("backend_type", backend_type_filter),
        "check_blank": identifier_config.get("check_blank_model_fields", False),
        "model_name_conversions": identifier_config.get(
            "backend_to_ts_model_name_conversions", {}
        ),
        "backend_models_to_ignore": identifier_config.get(
            "backend_models_to_ignore", []
        ),
    }


# MARK: Checks Function


def run_checks(
    config: dict, identifiers: list[str], backend_type_filter: str | None = None
) -> list[bool]:
    """
    Function to run checks for the given list of identifiers.

    Parameters
    ----------
    config : dict
        Get a dictionary of config paths.

    identifiers : list
        Get a list of identifiers.

    backend_type_filter : str | None
        The backend type to check against, either 'django' or 'fastapi'.

    Returns
    -------
    list[bool]
        Returns a list of boolean values that define whether checks have passed.
    """
    results: list[bool] = []
    if not backend_type_filter:
        rprint(
            "\n[red]❌  Please give a proper backend type command django or fastapi models to check against. [/red]"
        )
        sys.exit(1)
    for identifier in identifiers:
        identifier_config = config.get(identifier)
        if not identifier_config:
            rprint(
                f"[red]{identifier} is not an index within the .ts-backend-check.yaml "
                "configuration file. Please check the defined models and try again.[/red]"
            )
            sys.exit(1)

        extracted = extract_identifier_config(identifier_config, backend_type_filter)
        if extracted["backend_type"] != backend_type_filter:
            continue

        r = check_files_and_print_results(
            identifier=identifier,
            **extracted,
        )
        results.append(r)

    return results


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
    - --identifier (-i): The model-interface identifier in the .ts-backend-check.yaml configuration file to check.
    - --all (-a): Run checks of all backend models against their corresponding TypeScript interfaces.

    Examples
    --------
    >>> ts-backend-check --generate-config-file  # -gcf
    >>> ts-backend-check --identifier <model-interface-identifier-from-config-file>  # -i
    >>> ts-backend-check --backend_type <django|fastapi> # -b
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
        "-i",
        "--identifier",
        help="The model-interface identifier in the .ts-backend-check.yaml configuration file to check.",
    )

    parser.add_argument(
        "-b",
        "--backend-type",
        choices=["django", "fastapi"],
        default=None,
        help="The backend type to check against, either 'django' or 'fastapi'.",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run checks of all django or fastapi backend models against their corresponding TypeScript interfaces, requires -b or --backend-type django or fastapi.",
    )

    # MARK: Setup CLI

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args == ["--help"]:
        parser.print_help()

    YAML_CONFIG_FILE_PATH = get_config_file_path()

    if args.generate_test_project:
        generate_test_project()
        return

    if args.upgrade:
        upgrade_cli()
        return

    # MARK: CLI Variables

    if not Path(YAML_CONFIG_FILE_PATH).is_file() and args.generate_config_file:
        generate_config_file()
        return

    if not Path(YAML_CONFIG_FILE_PATH).is_file():
        print(
            "No configuration file. Please generate a configuration file (.ts-backend-check.yaml or .ts-backend-check.yml) with ts-backend-check -gcf."
        )
        exit(1)

    with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if args.generate_config_file:
        generate_config_file()
        return

    if not config_file_is_valid():
        sys.exit(1)

    # MARK: Run Checks

    results: list[bool] = []

    if args.identifier:
        identifiers = [args.identifier]

    elif args.all:
        identifiers = list(config.keys())

    else:
        rprint(
            "[red]CLI options not recognized. Please see the help directions below.[/red]"
        )
        parser.print_help()
        return

    results = run_checks(config, identifiers, args.backend_type)

    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
