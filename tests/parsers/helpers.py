# SPDX-License-Identifier: GPL-3.0-or-later
import re

from ts_backend_check.parsers.backend_parser import BackendModelParser, ModelData

"""
Initiate MinimalParser as a child of BackendModelParser to initiate method.
"""


class MinimalParser(BackendModelParser):
    MODEL_TEXT_REGEX = re.compile(r"BODY:(.*?):NAME:(\w+):END", re.DOTALL)
    ALL_MODEL_FIELDS_ORDERED_REGEX = re.compile(r".*")

    def _build_models(self, direct_fields, direct_blank_fields, inherited, model_lines):
        return ModelData(
            models_all_fields={},
            models_all_blank_fields={},
            models_all_fields_and_blank_fields_ordered={},
        )
