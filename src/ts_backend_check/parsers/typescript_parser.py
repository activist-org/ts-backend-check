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
    Represents a TypeScript interface with its fields and parent interfaces.
    """

    name: str
    fields: List[str]
    parents: List[str]


class TypeScriptParser:
    """
    Parser for TypeScript interface files.

    Parameters
    ----------
    file_path : str
        The file path for the TypeScript file to parse.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def parse_interfaces(self) -> Dict[str, TypeScriptInterface]:
        """
        Parse TypeScript interfaces from the file.

        Returns
        -------
        Dict[str, TypeScriptInterface]
            The interface parsed into a dictionary for future processing.
        """
        interfaces = {}
        interface_pattern = (
            r"(?:export\s+|declare\s+)?interface\s+(\w+)"
            r"(?:\s+extends\s+([^{]+))?\s*{([\s\S]*?)}"
        )

        for match in re.finditer(interface_pattern, self.content):
            name = match.group(1)
            parents = (
                [p.strip() for p in match.group(2).split(",")] if match.group(2) else []
            )
            fields = self._extract_fields(match.group(3))

            interfaces[name] = TypeScriptInterface(name, fields, parents)

        return interfaces

    def get_ignored_fields(self) -> Set[str]:
        """
        Extract fields marked as ignored in comments.

        Returns
        -------
        Set[str]
            The field names that are marked with a ts-backend-check-ignore identifier to ignore them.
        """
        ignore_pattern = r"//.*?ts-backend-check: ignore field\s+(\w+)"
        return set(re.findall(ignore_pattern, self.content))

    @staticmethod
    def _extract_fields(interface_body: str) -> List[str]:
        """
        Extract both real fields and 'ignored' comment fields from interface bodies.

        Parameters
        ----------
        interface_body : str
            A string representation of the interface body of the model.

        Returns
        -------
        List[str]
            The field names from the model interface body.
        """
        combined_pattern = (
            r"(?:(?:readonly\s+)?(\w+)\s*\??\s*:|"  # standard/readonly fields
            r"//.*?ts-backend-check:\s*ignore\s+field\s+(\w+))"  # ts-backend-check ignore comment fields
        )

        fields = []

        # finditer preserves the top-to-bottom order of the file.
        for match in re.finditer(combined_pattern, interface_body):
            if field_name := match.group(1) or match.group(2):
                fields.append(field_name)

        return fields
