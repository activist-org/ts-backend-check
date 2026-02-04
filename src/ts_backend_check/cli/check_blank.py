# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to check TypeScript interfaces for fields that should be optional based on Django models.
"""

import ast
from pathlib import Path
from typing import Dict, List

from rich.console import Console

from ts_backend_check.parsers.django_parser import DjangoModelVisitor

ROOT_DIR = Path.cwd()
console = Console()


def check_blank(file_path: str) -> Dict[str, List[str]]:
    """
    Function to extract fields from Django models file which accepts blank values.

    Parameters
    ----------
    file_path : str
        A models.py file that defines Django models.

    Returns
    -------
    Dict[str, List[str]]
        The fields from the models file extracted into a dictionary for future processing.
    """
    model_path = ROOT_DIR / file_path

    if model_path.is_file():
        with open(model_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # Skip any empty lines at the beginning.
            while content.startswith("\n"):
                content = content[1:]

        try:
            tree = ast.parse(content)

        except SyntaxError as e:
            raise SyntaxError(
                f"Failed to parse {model_path}. Make sure it's a valid Python file. Error: {str(e)}"
            ) from e

        parser = DjangoModelVisitor()
        parser.visit(tree)

        if len(parser.blank_models) == 0:
            console.print("[green]No models have any blank fields specified.[green]")

        else:
            for k, v in parser.blank_models.items():
                console.print(
                    f"[yellow]Model {k} has fields {sorted(v)} set as optional."
                )

    else:
        print("Check the path entered.")

    return parser.blank_models
