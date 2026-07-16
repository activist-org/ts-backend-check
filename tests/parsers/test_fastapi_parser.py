# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from ts_backend_check.parsers.backend_parser import ModelData
from ts_backend_check.parsers.fastapi_parser import FastAPIModelParser


# Regex Test
def test_extract_model_fields(return_invalid_fastapi_models):
    parser = FastAPIModelParser()
    fields = parser.parse(return_invalid_fastapi_models)

    assert "EventModel" in fields.models_all_fields
    event_fields = fields.models_all_fields["EventModel"]

    # Check that all non-private fields are extracted.
    assert "title" in event_fields
    assert "description" in event_fields
    assert "organizer" in event_fields
    assert "participants" in event_fields
    assert "is_private" in event_fields
    assert "date" in event_fields

    # Check that private fields are ignored.
    assert "_private_field" not in event_fields


def test_extract_model_fields_with_invalid_syntax(tmp_path):
    parser = FastAPIModelParser()
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        parser.parse(invalid_model)


def test_extract_model_fields_with_empty_file(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    parser = FastAPIModelParser()

    fields = parser.parse(empty_file)
    assert fields == ModelData()


def backend_models_to_ignore_from_config(return_invalid_django_models):
    parser = FastAPIModelParser()
    fields = parser.parse(return_invalid_django_models)
    assert fields.models_all_fields[0] == "BackendOnlyModel"
