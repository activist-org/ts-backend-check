# SPDX-License-Identifier: GPL-3.0-or-later

from ts_backend_check.checker import TypeChecker


def test_checker_finds_missing_fields(
    return_invalid_django_models, return_invalid_ts_interfaces
):
    checker = TypeChecker(return_invalid_django_models, return_invalid_ts_interfaces)
    missing = checker.check()

    # We know 'date' and 'participants' are marked as backend-only.
    # So they shouldn't be reported as missing.
    assert len(missing) == 0


def test_checker_with_actual_missing_fields(tmp_path):
    # Create a model with an extra field.
    model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    extra_field = models.IntegerField()
"""

    model_file = tmp_path / "test_model.py"
    model_file.write_text(model_content)

    # Create a type with missing field.
    type_content = """export interface Test {
    name: string;
}
"""

    type_file = tmp_path / "test_type.ts"
    type_file.write_text(type_content)

    checker = TypeChecker(str(model_file), str(type_file))
    missing = checker.check()

    assert len(missing) == 1
    assert "extra_field" in missing[0]


def test_checker_with_no_matching_interface(tmp_path):
    # Create a model.
    model_content = """from django.db import models

class UnmatchedModel(models.Model):
    name = models.CharField(max_length=100)
"""

    model_file = tmp_path / "unmatched_model.py"
    model_file.write_text(model_content)

    # Create a type file with no matching interface.
    type_content = """export interface DifferentInterface {
    something: string;
}
"""

    type_file = tmp_path / "unmatched_type.ts"
    type_file.write_text(type_content)

    checker = TypeChecker(str(model_file), str(type_file))
    missing = checker.check()

    assert len(missing) == 1
    assert (
        "No matching TypeScript interface found for model: UnmatchedModel" in missing[0]
    )
