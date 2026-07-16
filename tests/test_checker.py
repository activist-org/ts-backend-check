# SPDX-License-Identifier: GPL-3.0-or-later

import textwrap

import pytest

from ts_backend_check.checker import TypeChecker


@pytest.mark.parametrize(
    "backend_type,models,concatenated_types_file,check_blank_models,backend_to_ts_conversions,backend_models_to_ignore,expected_error_count",
    [
        pytest.param(
            "django",
            "return_invalid_django_models",
            "return_invalid_django_concatenated_types_file",
            "return_invalid_django_check_blank_models",
            "return_invalid_django_backend_to_ts_conversions",
            "return_invalid_django_backend_models_to_ignore",
            3,
            id="django",
        ),
        pytest.param(
            "fastapi",
            "return_invalid_fastapi_models",
            "return_invalid_fastapi_concatenated_types_file",
            "return_invalid_fastapi_check_blank_models",
            "return_invalid_fastapi_backend_to_ts_conversions",
            "return_invalid_fastapi_backend_models_to_ignore",
            3,
            id="fastapi",
        ),
    ],
)
def test_django_checker_invalid_checks_fail(
    request,
    backend_type,
    models,
    concatenated_types_file,
    check_blank_models,
    backend_to_ts_conversions,
    backend_models_to_ignore,
    expected_error_count,
):
    """
    Test that those checks that should fail in the invalid files do.
    """
    checker = TypeChecker(
        models_file=request.getfixturevalue(models),
        concatenated_types_file=request.getfixturevalue(concatenated_types_file),
        check_blank=request.getfixturevalue(check_blank_models),
        backend_type=backend_type,
        model_name_conversions=request.getfixturevalue(backend_to_ts_conversions),
        backend_models_to_ignore=request.getfixturevalue(backend_models_to_ignore),
    )
    errors = checker.check()

    assert (
        len(errors) == expected_error_count
    )  # missing, optional and no matching interface


@pytest.mark.parametrize(
    "backend_type,models,concatenated_types_file,check_blank_models,backend_to_ts_conversions,backend_models_to_ignore,expected_error_count",
    [
        pytest.param(
            "django",
            "return_valid_django_models",
            "return_valid_django_concatenated_types_file",
            "return_valid_django_check_blank_models",
            "return_valid_django_backend_to_ts_conversions",
            "return_valid_django_backend_models_to_ignore",
            0,
            id="django",
        ),
        pytest.param(
            "fastapi",
            "return_valid_fastapi_models",
            "return_valid_fastapi_concatenated_types_file",
            "return_valid_fastapi_check_blank_models",
            "return_valid_fastapi_backend_to_ts_conversions",
            "return_valid_fastapi_backend_models_to_ignore",
            0,
            id="fastapi",
        ),
    ],
)
def test_checker_ignored_missing_fields(
    request,
    backend_type,
    models,
    concatenated_types_file,
    check_blank_models,
    backend_to_ts_conversions,
    backend_models_to_ignore,
    expected_error_count,
):
    """
    Test that the ignore fields comment functions properly.
    """
    checker = TypeChecker(
        models_file=request.getfixturevalue(models),
        concatenated_types_file=request.getfixturevalue(concatenated_types_file),
        check_blank=request.getfixturevalue(check_blank_models),
        backend_type=backend_type,
        model_name_conversions=request.getfixturevalue(backend_to_ts_conversions),
        backend_models_to_ignore=request.getfixturevalue(backend_models_to_ignore),
    )
    errors = checker.check()

    # The field 'date' is marked as ignored by ts-backend-check.
    assert len(errors) == expected_error_count


@pytest.mark.parametrize(
    "backend_type,models,concatenated_types_file,check_blank_models,backend_to_ts_conversions,backend_models_to_ignore,expected_error_count",
    [
        pytest.param(
            "django",
            "return_invalid_django_models",
            "return_invalid_django_concatenated_types_file",
            "return_invalid_django_check_blank_models",
            "return_invalid_django_backend_to_ts_conversions",
            "return_invalid_django_backend_models_to_ignore",
            3,
            id="django",
        ),
        pytest.param(
            "fastapi",
            "return_invalid_fastapi_models",
            "return_invalid_fastapi_concatenated_types_file",
            "return_invalid_fastapi_check_blank_models",
            "return_invalid_fastapi_backend_to_ts_conversions",
            "return_invalid_fastapi_backend_models_to_ignore",
            3,
            id="fastapi",
        ),
    ],
)
def test_checker_with_actual_missing_fields(
    request,
    backend_type,
    models,
    concatenated_types_file,
    check_blank_models,
    backend_to_ts_conversions,
    backend_models_to_ignore,
    expected_error_count,
):
    """
    Check that missing fields are reported in invalid files.
    """
    checker = TypeChecker(
        models_file=request.getfixturevalue(models),
        concatenated_types_file=request.getfixturevalue(concatenated_types_file),
        check_blank=request.getfixturevalue(check_blank_models),
        backend_type=backend_type,
        model_name_conversions=request.getfixturevalue(backend_to_ts_conversions),
        backend_models_to_ignore=request.getfixturevalue(backend_models_to_ignore),
    )
    errors = checker.check()

    assert len(errors) == expected_error_count
    assert "description" in "".join(errors)


@pytest.mark.parametrize(
    "backend_type,models,concatenated_types_file,check_blank_models,backend_to_ts_conversions,backend_models_to_ignore,expected_error_count",
    [
        pytest.param(
            "django",
            "return_invalid_django_models",
            "return_invalid_django_concatenated_types_file",
            "return_invalid_django_check_blank_models",
            "return_invalid_django_backend_to_ts_conversions",
            "return_invalid_django_backend_models_to_ignore",
            3,
            id="django",
        ),
        pytest.param(
            "fastapi",
            "return_invalid_fastapi_models",
            "return_invalid_fastapi_concatenated_types_file",
            "return_invalid_fastapi_check_blank_models",
            "return_invalid_fastapi_backend_to_ts_conversions",
            "return_invalid_fastapi_backend_models_to_ignore",
            3,
            id="fastapi",
        ),
    ],
)
def test_checker_with_no_matching_interface(
    request,
    backend_type,
    models,
    concatenated_types_file,
    check_blank_models,
    backend_to_ts_conversions,
    backend_models_to_ignore,
    expected_error_count,
):
    """
    Check that missing interfaces will be reported.
    """
    checker = TypeChecker(
        models_file=request.getfixturevalue(models),
        concatenated_types_file=request.getfixturevalue(concatenated_types_file),
        check_blank=request.getfixturevalue(check_blank_models),
        backend_type=backend_type,
        model_name_conversions=request.getfixturevalue(backend_to_ts_conversions),
        backend_models_to_ignore=request.getfixturevalue(backend_models_to_ignore),
    )
    errors = checker.check()

    assert len(errors) == expected_error_count
    assert (
        "No matching TypeScript interface found for the model 'UserModel'."
        in "".join(errors)
    )


@pytest.mark.parametrize(
    "backend_type,model_content,expected",
    [
        pytest.param(
            "django",
            textwrap.dedent(
                """
            from django.db import models
            class ModelWithOrder(models.Model):
                name = models.CharField(max_length=100)
                description = models.CharField(max_length=100)
        """
            ),
            1,
            id="django",
        ),
        pytest.param(
            "fastapi",
            textwrap.dedent(
                """
            from pydantic import BaseModel
            class ModelWithOrder(BaseModel):
                name: str
                description: str
            """
            ),
            1,
            id="fastapi",
        ),
    ],
)
def test_checker_with_unordered_interface(
    tmp_path,
    backend_type,
    model_content,
    expected,
):
    """
    Test that the checker will report an unordered interface (isn't reported in the test project check).
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
        models_file=str(model_file),
        concatenated_types_file=concatenated_types_file,
        backend_type=backend_type,
    )
    errors = checker.check()

    assert len(errors) == expected
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


@pytest.mark.parametrize(
    "backend_type,models,concatenated_types_file,check_blank_models,backend_to_ts_conversions,backend_models_to_ignore,expected_error_count",
    [
        pytest.param(
            "django",
            "return_valid_django_models",
            "return_valid_django_concatenated_types_file",
            "return_valid_django_check_blank_models",
            "return_valid_django_backend_to_ts_conversions",
            "return_valid_django_backend_models_to_ignore",
            0,
            id="django",
        ),
        pytest.param(
            "fastapi",
            "return_valid_fastapi_models",
            "return_valid_fastapi_concatenated_types_file",
            "return_valid_fastapi_check_blank_models",
            "return_valid_fastapi_backend_to_ts_conversions",
            "return_valid_fastapi_backend_models_to_ignore",
            0,
            id="fastapi",
        ),
    ],
)
def test_checker_with_ignored_backend_models(
    request,
    backend_type,
    models,
    concatenated_types_file,
    check_blank_models,
    backend_to_ts_conversions,
    backend_models_to_ignore,
    expected_error_count,
):
    """
    Check that missing interfaces will be reported.
    """
    checker = TypeChecker(
        models_file=request.getfixturevalue(models),
        concatenated_types_file=request.getfixturevalue(concatenated_types_file),
        check_blank=request.getfixturevalue(check_blank_models),
        backend_type=backend_type,
        model_name_conversions=request.getfixturevalue(backend_to_ts_conversions),
        backend_models_to_ignore=request.getfixturevalue(backend_models_to_ignore),
    )
    errors = checker.check()

    assert len(errors) == expected_error_count
