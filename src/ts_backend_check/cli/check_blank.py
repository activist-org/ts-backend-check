# SPDX-License-Identifier: GPL-3.0-or-later
import ast
from pathlib import Path
from typing import Dict, Set

from rich.console import Console

ROOT_DIR = Path.cwd()
console = Console()


class BlankParser(ast.NodeVisitor):
    """
    AST visitor to extract fields from Django models.
    """

    DJANGO_FIELD_TYPES = {
        "Field",
        "CharField",
        "TextField",
        "IntegerField",
        "BooleanField",
        "DateTimeField",
        "ForeignKey",
        "ManyToManyField",
        "OneToOneField",
        "EmailField",
        "URLField",
        "FileField",
        "ImageField",
        "DecimalField",
        "AutoField",
    }

    def __init__(self) -> None:
        self.models: Dict[str, Set[str]] = {}
        self.current_model: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Check class definitions, specifically those that inherit from other classes.

        Parameters
        ----------
        node : ast.ClassDef
            A class definition from Python AST (Abstract Syntax Tree).
            It contains information about the class, such as its name, base classes, body, decorators, etc.
        """
        # Only process classes that inherit from something.
        if node.bases:
            self.current_model = node.name
            if self.current_model not in self.models:
                self.models[self.current_model] = set()

            self.generic_visit(node)

        self.current_model = None

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Check assignment statements within a class.

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
                self.models[self.current_model].add(target.id)


def check_blank(file_path: str) -> Dict[str, Set[str]]:
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

        for k, v in parser.models.items():
            if len(v) == 0:
                console.print(f"[green]Model {k} has no fields set as optional.[green]")
            else:
                console.print(
                    f"[yellow]Model {k} has fields {sorted(v)} set as optional."
                )

    else:
        print("Check the path entered.")

    return parser.models
