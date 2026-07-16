# SPDX-License-Identifier: GPL-3.0-or-later
"""
Module for parsing FastAPI models and extracting field information.
"""

import ast
import re
from typing import Any

from ts_backend_check.parsers.backend_parser import BackendModelParser, ModelData


class FastAPIModelParser(BackendModelParser):
    """
    Concrete implementation of BackendModelParser for parsing FastAPI models.
    """

    # fastapi specific model_text_regex to extract model class definitions.
    MODEL_TEXT_REGEX = re.compile(
        r"^(class\s+(\w+).+?)(?=\nclass|\Z)", re.MULTILINE | re.DOTALL
    )

    # fastapi specific regex to extract all model fields in order, including inherited fields.
    ALL_MODEL_FIELDS_ORDERED_REGEX = re.compile(
        r"(?:^\s{4}(?!_)(\w+)\s*:\s*[\w\[\], |]+)"  # type-annotated field only, not private
        r"|"
        r"(?:#\s*(?:tsbc|ts-backend-check): .*inherit\s+(\w+)(?:\s*\((blank=True)\))?)",  # inherited
        re.MULTILINE,
    )

    def parse(self, models_file: str) -> ModelData:
        """
        Parse the FastAPI models from the given file and return a ModelData object containing parsed information.

        Parameters
        ----------
        models_file : str
            The path to the FastAPI models file to be parsed.

        Returns
        -------
        ModelData
            A dataclass containing all fields, blank fields, and ordered fields for the parsed models using _build_models.
        """
        tree, content = self._load_ast(models_file)
        inherited = self._extract_inherited_fields(content)

        direct_fields: dict[str, list[Any]] = {}
        direct_blank_fields: dict[str, list[Any]] = {}

        model_lines = {
            match.group(2): match.group(1).strip()
            for match in self.MODEL_TEXT_REGEX.finditer(content)
        }

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            if self._should_ignore(node.name):
                continue
            fields: list = []
            blank_fields: list = []
            fields, blank_fields = self._visit_annassign(node, fields, blank_fields)
            direct_fields[node.name] = fields
            direct_blank_fields[node.name] = blank_fields
        return self._build_models(
            direct_fields, direct_blank_fields, inherited, model_lines
        )

    def _visit_annassign(
        self, node: ast.ClassDef, fields: list, blank_fields: list
    ) -> tuple[list[str], list[str | None]]:
        """
        Visit the AnnAssign nodes in the given AST node and extract field names and blank fields Pydantic specific.

        Parameters
        ----------
        node : ast.ClassDef
            The AST node representing a class definition.

        fields : list
            A list to store the names of the fields found in the class.

        blank_fields : list
            A list to store the names of the fields that are considered blank.

        Returns
        -------
        tuple[list[str], list[str | None]]
            A tuple containing two lists: field names and blank field names found in the class.
        """
        for stmt in node.body:
            if not isinstance(stmt, ast.AnnAssign):
                continue
            if not isinstance(stmt.target, ast.Name):
                continue
            field_name: str = stmt.target.id
            if field_name.startswith("_"):
                continue
            fields.append(field_name)
            if self._has_blank(stmt):
                blank_fields.append(field_name)
        return fields, blank_fields

    def _has_blank(self, stmt: ast.AnnAssign) -> bool:
        """
        Check if pydantic model has blank fields.

        Parameters
        ----------
        stmt : ast.AnnAssign
            The AST node representing an annotated assignment.

        Returns
        -------
        bool
            True if the field is considered blank, False otherwise.
        """
        # Check Optional in annotation example X: Optional[int]
        has_optional = self._check_subscript(stmt, value="Optional")
        if has_optional is True:
            return True

        # Check if Annotation has Optional example:  X: int | None
        if isinstance(stmt.annotation, ast.BinOp):
            if isinstance(stmt.annotation.op, ast.BitOr):
                left = stmt.annotation.left
                right = stmt.annotation.right
                is_optional: bool = self._is_none(left) or self._is_none(right)
                return is_optional
        return False

    def _is_none(self, node: ast.expr) -> bool:
        """
        Check if the given AST node represents a blank field (i.e., X: int | None).

        Parameters
        ----------
        node : ast.expr
            The AST node to check.

        Returns
        -------
        bool
            True if the node represents a blank field, False otherwise.
        """
        if isinstance(node, ast.Constant) and node.value is None:
            return True
        if isinstance(node, ast.Name) and node.id == "None":
            return True
        return False

    def _check_subscript(self, stmt: ast.AnnAssign, value: str) -> bool:
        """
        Check if the given AST node represents a subscript with the specified value (e.g., Optional).

        Parameters
        ----------
        stmt : ast.AnnAssign
            The AST node to check.

        value : str
            The value to check for in the subscript (e.g., "Optional").

        Returns
        -------
        bool
            True if the node represents a subscript with the specified value, False otherwise.
        """
        if isinstance(stmt.annotation, ast.Subscript):
            if isinstance(stmt.annotation.value, ast.Name):
                if stmt.annotation.value.id == value:
                    return True
        return False

    def _build_models(
        self,
        direct_fields: dict[str, list[Any]],
        direct_blank_fields: dict[str, list[Any]],
        inherited: dict[str, dict[str, list[Any]]],
        model_lines: dict[str, str],
    ) -> ModelData:
        """
        Build the final model data structure from the parsed fields, blank fields, inherited fields, and model lines.

        Parameters
        ----------
        direct_fields : dict[str, list[Any]]
            A dictionary containing direct fields for each model.

        direct_blank_fields : dict[str, list[Any]]
            A dictionary containing direct blank fields for each model.

        inherited : dict[str, dict[str, list[Any]]]
            A dictionary containing inherited fields and inherited blank fields for each model.

        model_lines : dict[str, str]
            A dictionary containing the lines of code for each model.

        Returns
        -------
        ModelData
            A dataclass containing all fields, blank fields, and all_fields_blank_fields_ordered fields for the parsed models.
        """
        all_models = set(list(direct_fields.keys()) + list(direct_blank_fields.keys()))
        models_all_fields_ordered: dict[str, list[Any]] = {
            m: [
                f[0] if f[0] != "" else f[1]
                for f in self.ALL_MODEL_FIELDS_ORDERED_REGEX.findall(model_lines[m])
            ]
            for m in all_models
            if m in model_lines
        }

        models_all_fields: dict[str, list[Any]] = {}
        models_all_blank_fields: dict[str, list[Any]] = {}

        for m in all_models:
            models_all_fields[m] = inherited.get(m, {}).get(
                "inherited_fields", []
            ) + direct_fields.get(m, [])
            models_all_blank_fields[m] = inherited.get(m, {}).get(
                "inherited_blank_fields", []
            ) + direct_blank_fields.get(m, [])
        return ModelData(
            models_all_fields=models_all_fields,
            models_all_blank_fields=models_all_blank_fields,
            models_all_fields_and_blank_fields_ordered=models_all_fields_ordered,
        )
