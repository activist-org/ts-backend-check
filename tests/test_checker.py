# SPDX-License-Identifier: GPL-3.0-or-later

from ts_backend_check.checker import TypeChecker


def test_checker_invalid_checks_fail(
    return_invalid_django_models,
    return_invalid_ts_interfaces,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
):
    """
    Test that those checks that should fail in the invalid files do.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        types_file=return_invalid_ts_interfaces,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
    )
    errors = checker.check()

    assert len(errors) == 3  # missing, optional and no matching interface


def test_checker_ignored_missing_fields(
    return_valid_django_models,
    return_valid_ts_interfaces,
    return_valid_check_blank_models,
    return_valid_backend_to_ts_conversions,
):
    """
    Test that the ignore fields comment functions properly.
    """
    checker = TypeChecker(
        models_file=return_valid_django_models,
        types_file=return_valid_ts_interfaces,
        check_blank=return_valid_check_blank_models,
        model_name_conversions=return_valid_backend_to_ts_conversions,
    )
    errors = checker.check()

    # The field 'date' is marked as ignored by ts-backend-check.
    assert len(errors) == 0


def test_checker_with_actual_missing_fields(
    return_invalid_django_models,
    return_invalid_ts_interfaces,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
):
    """
    Check that missing fields are reported in invalid files.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        types_file=return_invalid_ts_interfaces,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
    )
    errors = checker.check()

    assert len(errors) == 3
    assert "description" in errors[0]


def test_checker_with_no_matching_interface(
    return_invalid_django_models,
    return_invalid_ts_interfaces,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
):
    """
    Check that missing interfaces will be reported.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        types_file=return_invalid_ts_interfaces,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
    )
    errors = checker.check()

    assert len(errors) == 3
    assert (
        "No matching TypeScript interface found for the model 'UserModel'." in errors[2]
    )


def test_checker_with_unordered_interface(tmp_path):
    """
    Test that the checker will report an unordered interface (isn't reported in the test project check).
    """
    model_content = """from django.db import models

class ModelWithOrder(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
"""
    model_file = tmp_path / "ordered_model.py"
    model_file.write_text(model_content)

    # Create a type file with no the properties unordered.
    type_content = """export interface ModelWithOrder {
    description: string;
    name: string;
}
"""
    type_file = tmp_path / "unordered_interface_type.ts"
    type_file.write_text(type_content)

    checker = TypeChecker(models_file=str(model_file), types_file=str(type_file))
    errors = checker.check()

    assert len(errors) == 1
    assert "The properties of the interface file" in errors[0]
    assert "are unordered" in errors[0]
    assert (
        "All interface properties should exactly match the order of the corresponding fields"
        in errors[0]
    )
    assert (
        "If the model is synced with multiple interfaces, then their properties should follow the order prescribed by the model fields."
        in errors[0]
    )
