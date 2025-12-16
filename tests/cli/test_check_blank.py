# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from ts_backend_check.cli.check_blank import check_blank


def test_extract_blank_fields(tmp_path):
    model_content = """
from django.db import models


class UserFlag(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(
        "authentication.UserModel",
        on_delete=models.CASCADE,
        related_name="flagged_user",
    )
    name = models.CharField(blank=True, max_length=255)
    desc = models.CharField(max_length=255)
    created_by = models.ForeignKey("authentication.UserModel", on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
"""
    model_file = tmp_path / "models.py"
    model_file.write_text(model_content)

    fields = check_blank(model_file)
    assert "UserFlag" in fields

    event_fields = fields["UserFlag"]
    assert "name" in event_fields


def test_extract_incorrect_file_path(tmp_path):
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        check_blank(str(invalid_model))
