# SPDX-License-Identifier: GPL-3.0-or-later
"""
Module for parsing Django models and extracting field information.
"""

import ast
import re
from typing import Any, Dict, List, Tuple


class DjangoModelVisitor(ast.NodeVisitor):
    """
    AST visitor to extract fields from Django models.

    Parameters
    ----------
    models_to_ignore : List[str]
        Model classes to ignore, obtained from the config file.
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

    def __init__(self, models_to_ignore: list[str] | None) -> None:
        self.current_model: str | None = None
        self.models_and_fields: Dict[str, List[str]] = {}
        self.models_and_blank_fields: Dict[str, List[str]] = {}
        self.models_to_ignore: set[str] = set(models_to_ignore or [])

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Check class definitions, specifically those that inherit from other classes and not listed in ignore classes.

        Parameters
        ----------
        node : ast.ClassDef
            A class definition from Python AST (Abstract Syntax Tree).
            It contains information about the class, such as its name, base classes, body, decorators, etc.
        """
        # Only process classes that inherit from something and are not ignored.
        if node.bases and node.name not in self.models_to_ignore:
            self.current_model = node.name
            if self.current_model not in self.models_and_fields:
                self.models_and_fields[self.current_model] = []

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
                isinstance(target, ast.Name)
                and not target.id.startswith("_")
                and isinstance(node.value, ast.Call)
                and hasattr(node.value.func, "attr")
            ) and any(
                field_type in node.value.func.attr
                for field_type in self.DJANGO_FIELD_TYPES
            ):
                self.models_and_fields[self.current_model].append(target.id)
                if any(
                    kw.arg == "blank"
                    and isinstance(kw.value, ast.Constant)
                    and kw.value.value is True
                    for kw in node.value.keywords
                ):
                    if self.current_model not in self.models_and_blank_fields:
                        self.models_and_blank_fields[self.current_model] = []

                    self.models_and_blank_fields[self.current_model].append(target.id)


def extract_model_fields(
    models_file: str, models_to_ignore: List[str] | None
) -> Tuple[Dict[str, List[Any]], Dict[str, List[Any]], Dict[str, List[Any]]]:
    """
    Extract fields from Django models file.

    Parameters
    ----------
    models_file : str
        A models.py file that defines Django models.

    models_to_ignore : List[str]
        Model classes to ignore, obtained from the config file.

    Returns
    -------
    Tuple(Dict[str, List[Any]], Dict[str, List[Any]], Dict[str, List[Any]])
        The fields from the models file extracted into dictionaries for future processing.
    """
    with open(models_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # Skip any empty lines at the beginning.
        while content.startswith("\n"):
            content = content[1:]

    try:
        tree = ast.parse(content)

    except SyntaxError as e:
        raise SyntaxError(
            f"Failed to parse {models_file}. Make sure it's a valid Python file. Error: {str(e)}"
        ) from e

    visitor = DjangoModelVisitor(models_to_ignore=models_to_ignore)
    visitor.visit(tree)

    # Derive texts for all model classes.
    MODEL_TEXT_REGEX = re.compile(
        r"^(class\s+(\w+).+?)(?=\nclass|\Z)", re.MULTILINE | re.DOTALL
    )
    model_lines = {
        match.group(2): match.group(1).strip()
        for match in MODEL_TEXT_REGEX.finditer(content)
    }

    # Derive fields inherited from other classes via comments.
    INHERIT_COMMENT_REGEX = re.compile(
        r"#.*?(?:tsbc|ts-backend-check): .*inherit\s+(\w+)\b(?!\s*\(blank=True\))"
    )
    INHERIT_BLANK_COMMENT_REGEX = re.compile(
        r"#\s*?(?:tsbc|ts-backend-check): .*inherit\s+(\w+)\s+\((blank=True)\)"
    )

    model_inherited_fields = {}
    for k, v in model_lines.items():
        model_inherited_fields[k] = {
            "inherited_fields": INHERIT_COMMENT_REGEX.findall(v)
        }
        model_inherited_fields[k]["inherited_blank_fields"] = [
            match.group(1).strip() for match in INHERIT_BLANK_COMMENT_REGEX.finditer(v)
        ]

    # Derive all fields ordered.
    ALL_MODEL_FIELDS_ORDERED_REGEX = re.compile(
        r"(?:^\s*(?!\s*_)(\w+)\s*=\s*\w+)"  # field (not including private)
        r"|"
        r"(?:#\s*(?:tsbc|ts-backend-check):\s*inherit\s+(\w+)(?:\s*\((blank=True)\))?)",  # inherited
        re.MULTILINE,
    )
    models_all_fields_and_blank_fields_ordered = {
        m: [
            f[0] if f[0] != "" else f[1]
            for f in ALL_MODEL_FIELDS_ORDERED_REGEX.findall(model_lines[m])
        ]
        for m in set(
            list(visitor.models_and_fields.keys())
            + list(visitor.models_and_blank_fields.keys())
        )
    }

    # Combine all fields for the model.
    models_all_fields = {}
    models_all_blank_fields = {}
    for m in list(models_all_fields_and_blank_fields_ordered.keys()):
        models_all_fields[m] = model_inherited_fields.get(m, {}).get(
            "inherited_fields", []
        ) + visitor.models_and_fields.get(m, [])

        models_all_blank_fields[m] = model_inherited_fields.get(m, {}).get(
            "inherited_blank_fields", []
        ) + visitor.models_and_blank_fields.get(m, [])

    return (
        models_all_fields_and_blank_fields_ordered,
        models_all_fields,
        models_all_blank_fields,
    )
