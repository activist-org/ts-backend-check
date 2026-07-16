# SPDX-License-Identifier: GPL-3.0-or-later
"""
Module for parsing Django models and extracting field information.
"""

import ast
import re
from typing import Any

from ts_backend_check.parsers.backend_parser import BackendModelParser, ModelData


class DjangoModelParser(BackendModelParser):
    """
    Concrete implementation of BackendModelParser for parsing FastAPI models.
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

    # django specific model_text_regex to extract model class definitions
    MODEL_TEXT_REGEX = re.compile(
        r"^(class\s+(\w+).+?)(?=\nclass|\Z)", re.MULTILINE | re.DOTALL
    )

    # django specific regex to extract all model fields in order, including inherited fields
    ALL_MODEL_FIELDS_ORDERED_REGEX = re.compile(
        r"(?:^\s*(?!\s*_)(\w+)\s*=\s*\w+)"  # field (not including private)
        r"|"
        r"(?:#\s*(?:tsbc|ts-backend-check): .*inherit\s+(\w+)(?:\s*\((blank=True)\))?)",  # inherited
        re.MULTILINE,
    )

    def parse(self, models_file: str) -> ModelData:
        """
        Parse the Django models from the given file and return a ModelData object containing parsed information.

        Parameters
        ----------
        models_file : str
            The path to the Django models file to be parsed.

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
            if not node.bases:
                continue
            if self._should_ignore(node.name):
                continue
            fields: list = []
            blank_fields: list = []

            for stmt in node.body:
                if not isinstance(stmt, ast.Assign):
                    continue
                fields, blank_fields = self._visit_targets(stmt, fields, blank_fields)
            direct_fields[node.name] = fields
            direct_blank_fields[node.name] = blank_fields

        return self._build_models(
            direct_fields, direct_blank_fields, inherited, model_lines
        )

    def _visit_targets(
        self, stmt: ast.Assign, fields: list, blank_fields: list
    ) -> tuple[list[str], list[str | None]]:
        """
        Visit the targets of an assignment statement and extract field names and blank field names.

        Parameters
        ----------
        stmt : ast.Assign
            The ast node representing an assignment statement of the django model.

        fields : list
            A list to store the names of the fields found in the class.

        blank_fields : list
            A list to store the names of the fields that are considered blank.

        Returns
        -------
        tuple[list[str], list[str | None]]
            A tuple containing two lists: field names and blank field names found in the class.
        """
        for target in stmt.targets:
            self._validate_ast_instances(stmt, target, fields, blank_fields)
        return fields, blank_fields

    def _validate_ast_instances(
        self, stmt: ast.Assign, target: ast.expr, fields: list, blank_fields: list
    ) -> None:
        """
        Helper method to validate an ast instance to verify Django models.

        Parameters
        ----------
        stmt : ast.Assign
            The ast node representing an assignment statement of the django model.

        target : ast.expr
            The ast expression currently gets visited.

        fields : list
            A list to store the names of the fields found in the class.

        blank_fields : list
            A list to store the names of the fields that are considered blank.

        Returns
        -------
        None
            Mutates the fields and blank_fields in place.
        """
        if not isinstance(target, ast.Name):
            return
        if target.id.startswith("_"):
            return
        if not isinstance(stmt.value, ast.Call):
            return
        if not isinstance(stmt.value.func, ast.Attribute):
            return
        if not any(ft in stmt.value.func.attr for ft in self.DJANGO_FIELD_TYPES):
            return

        fields.append(target.id)

        if any(
            kw.arg == "blank"
            and isinstance(kw.value, ast.Constant)
            and kw.value.value is True
            for kw in stmt.value.keywords
        ):
            blank_fields.append(target.id)

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
            A dictionary mapping model names to their directly defined fields.

        direct_blank_fields : dict[str, list[Any]]
            A dictionary mapping model names to their directly defined blank fields.

        inherited : dict[str,dict[str,list[Any]]]
            A dictionary mapping model names to their inherited fields and blank fields.

        model_lines : dict[str,str]
            A dictionary mapping model names to their corresponding lines of code in the models file.

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
