=========
Changelog
=========

See the `releases for ts-backend-check <https://github.com/activist-org/ts-backend-check/releases>`_ for an up to date list of versions and their release dates.

``ts-backend-check`` tries to follow `semantic versioning <https://semver.org/>`_, a ``MAJOR.MINOR.PATCH`` version where increments are made of the:

* ``MAJOR`` version when we make incompatible API changes
* ``MINOR`` version when we add functionality in a backwards compatible manner
* ``PATCH`` version when we make backwards compatible bug fixes

Emojis for the following are chosen based on `gitmoji <https://gitmoji.dev/>`_.

ts-backend-check 1.5.0
======================

✨ Features
-----------

- Interface file paths can now be broken up over multiple files in the ``.ts-backend-check.yaml`` configuration file (`#39 <https://github.com/activist-org/ts-backend-check/issues/39>`_).
- Backend models can be ignored in the ``.ts-backend-check.yaml`` configuration file (`#40 <https://github.com/activist-org/ts-backend-check/issues/40>`_).
- The user is prompted to regenerate their ``.ts-backend-check.yaml`` if the file is found to be empty or is missing required arguments (`#41 <https://github.com/activist-org/ts-backend-check/issues/41>`_).
- The user is prompted to write a configuration file for the test project on generation (`#46 <https://github.com/activist-org/ts-backend-check/issues/46>`_).

♻️ Code Refactoring
-------------------

- The ``--model`` (``-m``) flag was renamed ``--identifier`` (``-i``) for clarity as we're passing a model-interface identifier to the CLI (`#42 <https://github.com/activist-org/ts-backend-check/issues/42>`_).
- The ``get_config_file_path`` function was moved to ``utils.py``.
- Messages to the user were improved and refactored given the changes above.

✅ Tests
--------

- Tests were refactored given the changes above.

ts-backend-check 1.4.4
======================

⬆️ Dependencies
---------------

- Update all dev and production dependencies.

ts-backend-check 1.4.3
======================

🐞 Bug Fixes
------------

- The configuration setup was being ran again after a successful creation of a config file (`#36 <https://github.com/activist-org/ts-backend-check/issues/36>`_).

ts-backend-check 1.4.2
======================

🐞 Bug Fixes
------------

- The configuration file was being saved to the install directory rather than the current working directory (`#33 <https://github.com/activist-org/ts-backend-check/issues/33>`_).

## ts-backend-check 1.4.1

🐞 Bug Fixes
------------

- The file paths were not being picked up when generating a configuration file (`#33 <https://github.com/activist-org/ts-backend-check/issues/33>`_).

ts-backend-check 1.4.0
======================

✨ Features
-----------

- The user is now able to access the CLI via ``tsbc`` for quicker commands.

🐞 Bug Fixes
------------

- The CLI wasn't printing help when the user entered no arguments without a configuration file.
- The values in ``backend_to_ts_model_name_conversions`` dictionaries were being saved as strings instead of lists (`#34 <https://github.com/activist-org/ts-backend-check/issues/34>`_).
- Type definitions were added to empty variables to assure that they're use appropriately.

ts-backend-check 1.3.2
======================

📝 Documentation
----------------

- All documentation for the package was updated to improve clarity (`#26 <https://github.com/activist-org/ts-backend-check/issues/26>`_).

ts-backend-check 1.3.1
======================

♻️ Code Refactoring
-------------------

- The skip comment for the CLI is now ``// ts-backend-check: ignore {fieldName}`` to shorten it.

✅ Tests
--------

- Local pre-commit hooks are now ran with `prek <https://prek.j178.dev/>`_ instead of ``pre-commit``.

ts-backend-check 1.3.0
======================

⬆️ Dependencies
---------------

- Dependencies were updated given dependabot warnings.
- Dependency management was switched over to using `uv <https://docs.astral.sh/uv/>`_.

ts-backend-check 1.2.2
======================

- Updated the spacing of the CLI outputs to improve readability.

ts-backend-check 1.2.1
======================

♻️ Code Refactoring
-------------------

- The comment to ignore fields within TypeScript interfaces has been updated to ``// ts-backend-check: ignore field {fieldName}``.
- The output messages were updated to improve clarity with regards to file names being compared as well as word choice.

✅ Tests
--------

- Tests were updated to account for the code refactoring.

📝 Documentation
----------------

- The readme and documentation files were updated to show the functionality of the package (`#20 <https://github.com/activist-org/ts-backend-check/issues/20>`_).

ts-backend-check 1.2.0
======================

✨ Features
-----------

- Adds the ability for the user to check the most recent version of the package via the CLI's version command and upgrade it via a simple CLI argument (`#12 <https://github.com/activist-org/ts-backend-check/issues/12>`_).
- The outputs of the CLI are colored using `Rich <https://github.com/Textualize/rich>`_ (`#10 <https://github.com/activist-org/ts-backend-check/issues/10>`_).
- The help message is now displayed to the user instead of an error when no arguments are passed to an execution of ``ts-backend-check`` (`#18 <https://github.com/activist-org/ts-backend-check/issues/18>`_).
- The CLI can now check if a Django model field can be set as blank and asserts that the corresponding field in TypeScript interfaces be optional (`#11 <https://github.com/activist-org/ts-backend-check/issues/11>`_).

⬆️ Dependencies
---------------

- Dependencies were updated due to detected vulnerabilities.

✅ Tests
--------

- Tests were expanded to account for the new features.

ts-backend-check 1.1.0
======================

✨ Features
-----------

- An argparse based CLI was developed (`#7 <https://github.com/activist-org/ts-backend-check/issues/7>`_) to help check TypeScript types against their corresponding backend models.
    * Arguments include passing a backend model file and a TypeScript file that should be compared.
    * The backend model fields are extracted, which currently works for Django based models.
    * These model fields are then compared against a TypeScript file to check if they have been mentioned in the code.
    * This process helps keep frontend and backend development processes in sync.

🎨 Design
---------

- A logo and icon have been designed for the package.

⚖️ Legal
--------

- The code has been appropriately licensed and includes SPDX license identifiers in all files.
- A security file has been added to the repo to make steps clear.

✅ Tests
--------

- Testing has been written for the CLI functionalities (`#2 <https://github.com/activist-org/ts-bachend-check/issues/2>`_).
- GitHub Actions based checks are used to validate file license headers, ruff based code formatting, mypy static type checking and pytest based tests on each pull request.
- pre-commit hooks are used to enforce code quality before commits during development.

📝 Documentation
----------------

- All onboarding documentation has been written including an extensive readme, a contributing guide and GitHub templates to help people contribute effectively.
- Read the Docs documentation has been generated for the project and can be found at `ts-backend-check.readthedocs.io <https://ts-backend-check.readthedocs.io/en/latest/>`_ (`#3 <https://github.com/activist-org/ts-bachend-check/issues/3>`_).
- All docstrings for functions and classes were standardized based on numpydoc.

♻️ Code Refactoring
------------------

- Code originally developed in the `activist-org/activist <https://github.com/activist-org/activist>`_ project was moved to a separate repo.

ts-backend-check 1.0.0
======================

- Initial release of the package to PyPI with a basic structure.
