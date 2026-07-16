# SPDX-License-Identifier: GPL-3.0-or-later
"""
Context class to select the appropriate parser based on the backend type.
"""

from ts_backend_check.parsers.backend_parser import ModelData
from ts_backend_check.parsers.django_parser import DjangoModelParser
from ts_backend_check.parsers.fastapi_parser import FastAPIModelParser


class ParserContext:
    """
    Context class to select the appropriate parser based on the backend type.

    Parameters
    ----------
    backend_type : str
        The type of backend for which the parser is to be selected. Supported values are "django" and "fastapi".

    models_to_ignore : list[str] | None
        A list of model names to ignore during parsing.
    """

    def __init__(self, backend_type: str, models_to_ignore: list[str] | None = None):
        if backend_type == "django":
            self._parser = DjangoModelParser(models_to_ignore)
        elif backend_type == "fastapi":
            self._parser = FastAPIModelParser(models_to_ignore)
        else:
            raise ValueError(f"Unsupported backend type: {backend_type}")

    def parse(self, models_file: str) -> ModelData:
        """
        Parse the models from the given file using the selected parser and return parsed data.

        Parameters
        ----------
        models_file : str
            The path to the models file to be parsed.

        Returns
        -------
        ModelData
            A dataclass containing all fields, blank fields, and ordered fields for the parsed models.
        """
        return self._parser.parse(models_file)
