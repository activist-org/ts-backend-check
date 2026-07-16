# SPDX-License-Identifier: GPL-3.0-or-later
"""
Abstract Model for Backend parsers to parse Django and FastAPI models.
"""

import ast
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelData:
    """
    A dataclass to hold the parsed model data, including all fields, blank fields and ordered fields.
    """

    models_all_fields: dict = field(default_factory=dict)
    models_all_blank_fields: dict = field(default_factory=dict)
    models_all_fields_and_blank_fields_ordered: dict = field(default_factory=dict)


class BackendModelParser(ABC):
    """
    Abstract base class for parsing backend models.

    Parameters
    ----------
    models_to_ignore : list[str]
        A list of model names to ignore during parsing.
    """

    # Derive fields inherited from other classes via comments.
    INHERIT_FIELD_COMMENT_REGEX = re.compile(
        r"#.*?(?:tsbc|ts-backend-check): .*inherit\s+(\w+)\b(?!\s*\(blank=True\))"
    )
    INHERIT_BLANK_FIELD_COMMENT_REGEX = re.compile(
        r"#\s*?(?:tsbc|ts-backend-check): .*inherit\s+(\w+)\s+\((blank=True)\)"
    )

    def __init__(self, models_to_ignore: list[str] | None = None):
        self.models_to_ignore = models_to_ignore

    @property
    @abstractmethod
    def MODEL_TEXT_REGEX(self) -> re.Pattern:
        """
        Abstract property to be implemented by subclasses.

        Returns
        -------
        re.Pattern
            A compiled regex pattern for matching model definitions.
        """
        ...

    def _load_ast(self, models_file: str) -> tuple[ast.Module, str]:
        """
        Load the AST from the given models file.

        Parameters
        ----------
        models_file : str
            The path to the models file to be parsed.

        Returns
        -------
        tuple[ast.module, str]
            A tuple containing the parsed AST and the content of the models file.
        """
        with open(models_file, encoding="utf-8") as file:
            content = file.read().strip()
            # Skip any empty lines at the beginning.
            while content.startswith("\n"):
                content = content[1:]

        try:
            tree = ast.parse(content)

        except SyntaxError as e:
            raise SyntaxError(
                f"Failed to parse {models_file}. Make sure it's a valid Python file. Error: {str(e)}"
            ) from e
        return (tree, content)

    def _should_ignore(self, class_name: str) -> bool:
        """
        Check if a given class name should be ignored based on the models_to_ignore list.

        Parameters
        ----------
        class_name : str
            The name of the class to check.

        Returns
        -------
        bool
            True if the class name is in the models_to_ignore list, False otherwise.
        """
        return class_name in self.models_to_ignore if self.models_to_ignore else False

    def _extract_inherited_fields(
        self, content: str
    ) -> dict[str, dict[str, list[Any]]]:
        """
        Extract inherited fields from the model definitions in the given content.

        Parameters
        ----------
        content : str
            The content of the models file to be parsed in string format.

        Returns
        -------
        dict[str, dict[str, list[Any]]]
            A dictionary where keys are model names and values are dictionaries containing inherited fields and inherited blank fields.
        """
        model_lines = {
            match.group(2): match.group(1).strip()
            for match in self.MODEL_TEXT_REGEX.finditer(content)
        }

        inherited: dict[str, dict[str, list[Any]]] = {}
        for model_name, text in model_lines.items():
            inherited[model_name] = {
                "inherited_fields": self.INHERIT_FIELD_COMMENT_REGEX.findall(text),
                "inherited_blank_fields": [
                    m.group(1).strip()
                    for m in self.INHERIT_BLANK_FIELD_COMMENT_REGEX.finditer(text)
                ],
            }
        return inherited

    @property
    @abstractmethod
    def ALL_MODEL_FIELDS_ORDERED_REGEX(self) -> re.Pattern:
        """
        Abstract property to be implemented by subclasses.

        Returns
        -------
        re.Pattern
            A compiled regex pattern for matching all model fields in the backend models.
        """
        ...

    @abstractmethod
    def _build_models(
        self,
        direct_fields: dict[str, list[Any]],
        direct_blank_fields: dict[str, list[Any]],
        inherited: dict[str, dict[str, list[Any]]],
        model_lines: dict[str, str],
    ) -> ModelData:
        """
        Abstract method to be implemented by subclasses.

        Parameters
        ----------
        direct_fields : dict[str, list[Any]]
            A dictionary of direct fields for each model.

        direct_blank_fields : dict[str, list[Any]]
            A dictionary of direct blank fields for each model.

        inherited : dict[str, dict[str, list[Any]]]
            A dictionary of inherited fields and blank fields for each model.

        model_lines : dict[str, str]
            A dictionary of model names and their corresponding text lines from the models file.

        Returns
        -------
        ModelData
            A dataclass containing all fields, blank fields, and ordered fields for the parsed models.
        """
        ...
