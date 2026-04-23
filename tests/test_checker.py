# SPDX-License-Identifier: GPL-3.0-or-later

from ts_backend_check.checker import TypeChecker


def test_checker_invalid_checks_fail(
    return_invalid_django_models,
    return_invalid_concatenated_types_file,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
    return_invalid_backend_models_to_ignore,
):
    """
    Test that those checks that should fail in the invalid files do.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        concatenated_types_file=return_invalid_concatenated_types_file,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
        backend_models_to_ignore=return_invalid_backend_models_to_ignore,
    )
    errors = checker.check()

    assert len(errors) == 3  # missing, optional and no matching interface


def test_checker_ignored_missing_fields(
    return_valid_django_models,
    return_valid_concatenated_types_file,
    return_valid_check_blank_models,
    return_valid_backend_to_ts_conversions,
    return_valid_backend_models_to_ignore,
):
    """
    Test that the ignore fields comment functions properly.
    """
    checker = TypeChecker(
        models_file=return_valid_django_models,
        concatenated_types_file=return_valid_concatenated_types_file,
        check_blank=return_valid_check_blank_models,
        model_name_conversions=return_valid_backend_to_ts_conversions,
        backend_models_to_ignore=return_valid_backend_models_to_ignore,
    )
    errors = checker.check()

    # The field 'date' is marked as ignored by ts-backend-check.
    assert len(errors) == 0


def test_checker_with_actual_missing_fields(
    return_invalid_django_models,
    return_invalid_concatenated_types_file,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
    return_invalid_backend_models_to_ignore,
):
    """
    Check that missing fields are reported in invalid files.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        concatenated_types_file=return_invalid_concatenated_types_file,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
        backend_models_to_ignore=return_invalid_backend_models_to_ignore,
    )
    errors = checker.check()

    assert len(errors) == 3
    assert "description" in errors[0]


def test_checker_with_no_matching_interface(
    return_invalid_django_models,
    return_invalid_concatenated_types_file,
    return_invalid_check_blank_models,
    return_invalid_backend_to_ts_conversions,
    return_invalid_backend_models_to_ignore,
):
    """
    Check that missing interfaces will be reported.
    """
    checker = TypeChecker(
        models_file=return_invalid_django_models,
        concatenated_types_file=return_invalid_concatenated_types_file,
        check_blank=return_invalid_check_blank_models,
        model_name_conversions=return_invalid_backend_to_ts_conversions,
        backend_models_to_ignore=return_invalid_backend_models_to_ignore,
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

    with open(type_file, "r", encoding="utf-8") as f:
        concatenated_types_file = f.read()

    checker = TypeChecker(
        models_file=str(model_file), concatenated_types_file=concatenated_types_file
    )
    errors = checker.check()

    assert len(errors) == 1
    assert "The interface properties of the 'ts_interface_paths' files" in errors[0]
    assert "are unordered" in errors[0]
    assert (
        "All interface properties should exactly match the order of the corresponding fields"
        in errors[0]
    )
    assert (
        "If the model is synced with multiple interfaces, then their properties should follow the order prescribed by the model fields."
        in errors[0]
    )


def test_checker_with_ignored_backend_models(
    return_valid_django_models,
    return_valid_concatenated_types_file,
    return_valid_check_blank_models,
    return_valid_backend_to_ts_conversions,
    return_valid_backend_models_to_ignore,
):
    """
    Check that missing interfaces will be reported.
    """
    checker = TypeChecker(
        models_file=return_valid_django_models,
        concatenated_types_file=return_valid_concatenated_types_file,
        check_blank=return_valid_check_blank_models,
        model_name_conversions=return_valid_backend_to_ts_conversions,
        backend_models_to_ignore=return_valid_backend_models_to_ignore,
    )
    errors = checker.check()

    assert len(errors) == 0
