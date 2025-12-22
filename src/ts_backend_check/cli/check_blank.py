# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to check TypeScript interfaces for fields that should be optional based on Django models.
"""

import ast
from pathlib import Path
from typing import Dict, Set

from rich.console import Console

from ts_backend_check.parsers.django_parser import DjangoModelVisitor

ROOT_DIR = Path.cwd()
console = Console()


class BlankParser(DjangoModelVisitor):
    """
    AST visitor to extract blank fields from Django models based on DjangoModelVisitor.
    """

    def __init__(self) -> None:
        super().__init__()
        self.blank_models: Dict[str, Set[str]] = {}

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Check assignment statements within a class which accepts blank fields.

        Parameters
        ----------
        node : ast.Assign
            An assignment definition from Python AST (Abstract Syntax Tree).
            It represents an assignment statement (e.g., x = 42).
        """
        if not self.current_model:
            return

        for target in node.targets:
            if (
                (
                    isinstance(target, ast.Name)
                    and not target.id.startswith("_")
                    and isinstance(node.value, ast.Call)
                    and hasattr(node.value.func, "attr")
                )
                and any(
                    field_type in node.value.func.attr
                    for field_type in self.DJANGO_FIELD_TYPES
                )
                and any(
                    kw.arg == "blank"
                    and isinstance(kw.value, ast.Constant)
                    and kw.value.value is True
                    for kw in node.value.keywords
                )
            ):
                if self.current_model not in self.blank_models:
                    self.blank_models[self.current_model] = set()

                self.blank_models[self.current_model].add(target.id)


def check_blank(file_path: str) -> Dict[str, Set[str]]:
    """
    Function to extract fields from Django models file which accepts blank values.

    Parameters
    ----------
    file_path : str
        A models.py file that defines Django models.

    Returns
    -------
    Dict[str, Set[str]]
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

        parser = BlankParser()
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
