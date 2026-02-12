<div align="center">
  <a href="https://github.com/activist-org/ts-backend-check"><img src="https://raw.githubusercontent.com/activist-org/ts-backend-check/main/.github/resources/TSBackendCheckGitHubBanner.png" width=1024 alt="TS Backend Check logo"></a>
</div>

[![rtd](https://img.shields.io/readthedocs/ts-backend-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff)](http://ts-backend-check.readthedocs.io/en/latest/)
[![pr_ci](https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/pr_ci.yaml?branch=main&label=%20&logo=ruff&logoColor=ffffff)](https://github.com/activist-org/ts-backend-check/actions/workflows/pr_ci.yaml)
[![python_package_ci](https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/python_package_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff)](https://github.com/activist-org/ts-backend-check/actions/workflows/python_package_ci.yaml)
[![issues](https://img.shields.io/github/issues/activist-org/ts-backend-check?label=%20&logo=github)](https://github.com/activist-org/ts-backend-check/issues)
[![python](https://img.shields.io/badge/Python-4B8BBE.svg?logo=python&logoColor=ffffff)](https://github.com/activist-org/ts-backend-check/blob/main/CONTRIBUTING.md)
[![pypi](https://img.shields.io/pypi/v/ts-backend-check.svg?label=%20&color=4B8BBE)](https://pypi.org/project/ts-backend-check/)
[![pypistatus](https://img.shields.io/pypi/status/ts-backend-check.svg?label=%20)](https://pypi.org/project/ts-backend-check/)
[![license](https://img.shields.io/github/license/activist-org/ts-backend-check.svg?label=%20)](https://github.com/activist-org/ts-backend-check/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg)](https://github.com/activist-org/ts-backend-check/blob/main/.github/CODE_OF_CONDUCT.md)
[![matrix](https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff)](https://matrix.to/#/#activist_community:matrix.org)

# Contents

- [About ts-backend-check](#about-ts-backend-check)
- [Installation](#installation)
  - [Users](#users)
  - [Development Build](#development-build)
- [How It Works](#how-it-works)
  - [Commands](#commands)
  - [Example Outputs](#example-outputs)
- [Configuration](#configuration)
  - [YAML File](#yaml-file)
  - [pre-commit](#pre-commit)
  - [GitHub Action](#github-action)
- [Contributing](#contributing)
  - [Contact the Team](#contact-the-team)
  - [Contributors](#contributors)

# About ts-backend-check

`ts-backend-check` is a Python package for checking TypeScript types against their corresponding backend models to assure that all fields have been accounted for.

Developed by the [activist community](https://github.com/activist-org), this package helps keep frontend and backend development teams in sync.

The package supports Django-based backends.

# Installation

## Users

You can install `ts-backend-check` using [uv](https://docs.astral.sh/uv/) (recommended) or [pip](https://pypi.org/project/ts-backend-check/).

### uv

(Recommended - fast, Rust-based installer)

```bash
uv pip install ts-backend-check
```

### pip

```bash
pip install ts-backend-check
```

## Development Build

You can install the latest development build using uv, pip, or by cloning the repository.

### Clone the Repository (Development Build)

```bash
git clone https://github.com/activist-org/ts-backend-check.git  # or ideally your fork
cd ts-backend-check
```

### uv (Development Build)

```bash
uv sync --all-extras  # install all dependencies
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)
```

### pip (Development Build)

```bash
python -m venv .venv  # create virtual environment
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)
pip install -e .
```

<sub><a href="#top">Back to top.</a></sub>

# How It Works

## Commands

These are some example commands:

**Show Help and Available Commands**

```bash
ts-backend-check --help
```

**Generate a Configuration File**

```bash
ts-backend-check -gcf
```

**Generate a Test Project**

```bash
ts-backend-check -gtp
```

**Check a TypeScript Type Against a Backend Model**

```bash
ts-backend-check -m <model-identifier-from-config-file>
```

**Run All Models**

```bash
ts-backend-check -a
```

## Example Outputs

These are some example outputs for passed and failed checks.

### Passed Check

```
ts-backend-check -m valid_model
✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided 'valid_model' files.
```

### Failed Check

```
ts-backend-check -m invalid_model

❌ ts-backend-check error: There are inconsistencies between the provided 'invalid_model' backend models and TypeScript interfaces. Please see the output below for
details.

Field 'description' (camelCase: 'description') from model 'EventModel' is missing in the TypeScript interfaces.
Expected to find this field in the frontend interfaces: Event, EventExtended
To ignore this field, add the following comment to the TypeScript file (in order based on the model fields): '// ts-backend-check: ignore description'

Field 'participants' (camelCase: 'participants') from model 'EventModel' doesn't match the TypeScript interfaces based on blank to optional agreement.
Please check 'src/ts_backend_check/test_project/backend/models.py' and 'src/ts_backend_check/test_project/frontend/invalid_interfaces.ts' to make sure that all
'blank=True' fields are optional (?) in the TypeScript interfaces file.

No matching TypeScript interface found for the model 'UserModel'.
Please name your TypeScript interfaces the same as the corresponding backend models.
You can also use the 'backend_to_ts_model_name_conversions' option within the configuration file.
The key is the backend model name and the value is a list of the corresponding interfaces.
This option is also how you can break larger backend models into multiple interfaces that extend one another.

Please fix the 3 errors above to continue the sync of the backend models of src/ts_backend_check/test_project/backend/models.py and the TypeScript interfaces of
src/ts_backend_check/test_project/frontend/invalid_interfaces.ts.
```

<sub><a href="#top">Back to top.</a></sub>

# Configuration

## YAML File

You can configure `ts-backend-check` using the `.ts-backend.check.yaml` (or `.yml`) configuration file.

For an example, see the [configuration file for this repository](/.ts-backend-check.yaml) that we use in testing.

This example describes the structure of an entry in this file:

```yaml
model_identifier: # an identifier you define that you want to pass to the CLI
  backend_model_path: path/to/a/models.py
  ts_interface_path: path/to/the/corresponding/model_interfaces.ts
  check_blank_model_fields: true # whether to assert that fields that can be blank must also be optional
  backend_to_ts_model_name_conversions: # used if the frontend name is not the backend name
    BackendModel: [Interface, InterfaceExtended]
```

## pre-commit

This is an exaple of a [prek](https://prek.j178.dev/) or [pre-commit](https://github.com/pre-commit/pre-commit) hook:

```yaml
- repo: local
  hooks:
    - id: run-ts-backend-check
      name: run ts-backend-check key-value checks
      files: ^src-dir/
      entry: ts-backend-check -a
      language: python
      pass_filenames: false
      additional_dependencies:
        - ts-backend-check
```

## GitHub Action

This is an example YAML file for a GitHub Action to check your backend models and TypeScript interface files on pull requests and commits:

```yaml
name: pr_ci_ts_backend_check
on:
  workflow_dispatch:
  pull_request:
    branches:
      - main
    types:
      - opened
      - reopened
      - synchronize
  push:
    branches:
      - main

jobs:
  ts_backend_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Project
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v7

      - name: Install Dependencies
        run: uv sync --frozen --all-extras

      - name: Execute All ts-backend-check Key-Value Checks
        run: |
          uv run ts-backend-check -a
```

<sub><a href="#top">Back to top.</a></sub>

# Contributing

See the [contribution guidelines](CONTRIBUTING.md) before contributing. You can help by:

- 🐞 Reporting bugs.
- ✨ Working with us on new features.
- 📝 Improving the documentation.

We track work that is in progress or may be implemented in the the [issues](https://github.com/activist-org/ts-backend-check/issues) and [projects](https://github.com/activist-org/ts-backend-check/projects).

## Contact the Team

<a href="https://matrix.to/#/#activist_community:matrix.org"><img src="https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png" width="175" alt="Public Matrix Chat" align="right"></a>

activist uses [Matrix](https://matrix.org/) for team communication. [Join us in our public chat rooms](https://matrix.to/#/#activist_community:matrix.org) to share ideas, ask questions or just say hi to the team.

We recommend using the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app.

## Contributors

Thanks to all our amazing [contributors](https://github.com/activist-org/ts-backend-check/graphs/contributors)! ❤️

<a href="https://github.com/activist-org/ts-backend-check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=activist-org/ts-backend-check" />
</a>

<sub><a href="#top">Back to top.</a></sub>
