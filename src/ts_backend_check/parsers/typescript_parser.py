# SPDX-License-Identifier: GPL-3.0-or-later
"""
Module for parsing TypeScript interfaces and types.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class TypeScriptInterface:
    """
    Represents a TypeScript interface with its properties and parent interfaces.
    """

    name: str
    properties: List[str]
    optional_properties: List[str]
    parents: List[str]


class TypeScriptParser:
    """
    Parser for TypeScript interface files.

    Parameters
    ----------
    concatenated_types_file : str
        The file path for the TypeScript file to parse.
    """

    def __init__(self, concatenated_types_file: str) -> None:
        self.content = concatenated_types_file

    def parse_interfaces(self) -> Dict[str, TypeScriptInterface]:
        """
        Parse TypeScript interfaces from the file.

        Returns
        -------
        Dict[str, TypeScriptInterface]
            The interface parsed into a dictionary for future processing.
        """
        interfaces: Dict[str, TypeScriptInterface] = {}
        interface_pattern = (
            r"(?:export\s+|declare\s+)?interface\s+(\w+)"
            r"(?:\s+extends\s+([^{]+))?\s*{([\s\S]*?)}"
        )

        for match in re.finditer(interface_pattern, self.content):
            name = match.group(1)
            parents = (
                [p.strip() for p in match.group(2).split(",")] if match.group(2) else []
            )
            properties = self._extract_properties(match.group(3))
            optional_properties = self._extract_optional_properties(match.group(3))

            interfaces[name] = TypeScriptInterface(
                name, properties, optional_properties, parents
            )

        return interfaces

    def get_ignored_fields(self) -> Set[str]:
        """
        Extract fields marked as ignored in comments.

        Returns
        -------
        Set[str]
            The field names that are marked with a ts-backend-check ignore identifier.
        """
        ignore_pattern = r"//.*?(?:tsbc|ts-backend-check): ignore\s+(\w+)"
        return set(re.findall(ignore_pattern, self.content))

    @staticmethod
    def _extract_properties(interface_body: str) -> List[str]:
        """
        Extract both real properties and 'ignored' comment backend fields from interface bodies.

        Parameters
        ----------
        interface_body : str
            A string representation of the interface body of the model.

        Returns
        -------
        List[str]
            The property names from the model interface body.
        """
        combined_pattern = (
            r"^\s*(?:"
            r"(?:readonly\s+)?(\w+)\s*\??\s*:|"  # standard/readonly properties
            r"//\s*ts-backend-check:\s*ignore\s+(\w+)"  # ts-backend-check ignore comment properties
            r")"
        )

        properties: list[str] = []
        for match in re.finditer(combined_pattern, interface_body, flags=re.MULTILINE):
            if field_name := match.group(1) or match.group(2):
                properties.append(field_name)

        return properties

    @staticmethod
    def _extract_optional_properties(interface_body: str) -> List[str]:
        """
        Extract all optional properties from interface bodies.

        Parameters
        ----------
        interface_body : str
            A string representation of the interface body of the model.

        Returns
        -------
        List[str]
            The optional property names from the model interface body.
        """
        pattern = r"^\s*(?:readonly\s+)?(\w+)\s*\?:"  # optional properties

        optional_properties: list[str] = []
        for match in re.finditer(pattern, interface_body, flags=re.MULTILINE):
            if field_name := match.group(1):
                optional_properties.append(field_name)

        return optional_properties
