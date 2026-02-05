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

### Check TypeScript interfaces against backend models

`ts-backend-check` is a Python package used to check TypeScript types against their corresponding backend models to assure that all fields have been accounted for.

Developed by the [activist community](https://github.com/activist-org), this package is meant to help synchronize the work between frontend and backend development teams. Currently the process supports Django based backends.

<a id="contents"></a>

# **Contents**

- [Usage](#usage-)
  - [Command Options](#command-options-)
  - [Outputs](#outputs-)
- [Installation](#installation-)
- [Configuration](#configuration-)
- [Contributing](#contributing-)
- [Environment setup](#environment-setup-)
- [Contributors](#contributors-)

<a id="usage-"></a>

## Usage [`⇧`](#contents)

<a id="command-options-"></a>

### Command Options [`⇧`](#contents)

The CLI provides a simple interface to check TypeScript types against backend models:

```bash
# Show help and available commands:
ts-backend-check --help
ts-backend-check -gcf  # generate a configuration file
ts-backend-check -gtp  # generate a test project for experimenting with the CLI

# Check a TypeScript type against a backend model:
ts-backend-check -m <model-identifier-from-config-file>
ts-backend-check -a  # run all models
```

<a id="outputs-"></a>

### Outputs [`⇧`](#contents)

Example success and error outputs for the CLI are:

```
ts-backend-check -m user
✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided files.
```

```
ts-backend-check -m user

❌ ts-backend-check error: There are inconsistencies between the provided backend models and TypeScript interfaces. Please see the output below for details.

Field 'user_name' (camelCase: 'userName') from model 'UserModel' is missing in the TypeScript interfaces.
Expected to find this field in the frontend interface: User
To ignore this field, add the following comment to the TypeScript interface: '// ts-backend-check: ignore field userName'

Please fix the 1 error above to have the backend models of backend/models/user.py synced with the TypeScript interfaces of frontend/types/user.ts.
```

<a id="installation-"></a>

## Installation

`ts-backend-check` is available for installation via [uv](https://docs.astral.sh/uv/) (recommended) or [pip](https://pypi.org/project/ts-backend-check/).

### For Users

```bash
# Using uv (recommended - fast, Rust-based installer):
uv pip install ts-backend-check

# Or using pip:
pip install ts-backend-check
```

### For Development Build

```bash
git clone https://github.com/activist-org/ts-backend-check.git  # or ideally your fork
cd ts-backend-check

# With uv (recommended):
uv sync --all-extras  # install all dependencies
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)

# Or with pip:
python -m venv .venv  # create virtual environment
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)
pip install -e .
```

<a id="configuration-"></a>

# Configuration [`⇧`](#contents)

ts-backend-check is configured via a `.ts-backend.check.yaml` (or `.yml`) configuration file, with an example being the [configuration file for this repository](/.ts-backend-check.yaml) that we use in testing. The following describes the structure of an entry in this file:

```yaml
model_identifier: # an identifier you define that you want to pass to the CLI
  backend_model_path: path/to/a/models.py
  ts_interface_path: path/to/the/corresponding/model_interfaces.ts
  check_blank_model_fields: true # whether to assert that fields that can be blank must also be optional
  backend_to_ts_model_name_conversions: # used if the frontend name is not the backend name
    EventModel: [CommunityEvent]
```

<a id="pre-commit-"></a>

### pre-commit [`⇧`](#contents)

The following is an example [pre-commit](https://github.com/pre-commit/pre-commit) hook:

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

<a id="github-action-"></a>

### GitHub Action [`⇧`](#contents)

The following is an example YAML file for a GitHub Action to check your backend models and TypeScript interface files on PRs and commits:

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

<a id="contributing-"></a>

# Contributing [`⇧`](#contents)

<a href="https://matrix.to/#/#activist_community:matrix.org"><img src="https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png" width="175" alt="Public Matrix Chat" align="right"></a>

activist uses [Matrix](https://matrix.org/) for internal communication. You're more than welcome to [join us in our public chat rooms](https://matrix.to/#/#activist_community:matrix.org) to share ideas, ask questions or just say hi to the team :) We'd suggest that you use the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app.

Please see the [contribution guide](CONTRIBUTING.md) if you are interested in contributing. Work that is in progress or could be implemented is tracked in the [issues](https://github.com/activist-org/ts-backend-check/issues) and [projects](https://github.com/activist-org/ts-backend-check/projects).

> [!NOTE]
> Just because an issue is assigned on GitHub doesn't mean the team isn't open to your contribution! Feel free to write [in the issues](https://github.com/activist-org/ts-backend-check/issues) and we can potentially reassign it to you.

Also check the [`-next release-`](https://github.com/activist-org/ts-backend-check/labels/-next%20release-) and [`-priority-`](https://github.com/activist-org/ts-backend-check/labels/-priority-) labels in the [issues](https://github.com/activist-org/ts-backend-check/issues) for those that are most important, as well as those marked [`good first issue`](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) that are tailored for first-time contributors. For those new to coding or our tech stack, we've collected [links to helpful documentation pages](CONTRIBUTING.md#learning-the-tech-stack-) in the [contribution guide](CONTRIBUTING.md).

We would be happy to discuss granting you further rights as a contributor after your first pull requests, with a maintainer role then being possible after continued interest in the project. activist seeks to be an inclusive, diverse and supportive organization. We'd love to have you on the team! Please see the [mentorship and growth section of the contribution guide](CONTRIBUTING.md#mentorship-and-growth-) for further information.

<a id="how-you-can-help-"></a>

## How you can help [`⇧`](#contents)

- [Reporting bugs](https://github.com/activist-org/ts-backend-check/issues/new?assignees=&labels=bug&template=bug_report.yml) as they're found 🐞
- Working with us on [new features](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3Afeature) ✨
- [Documentation](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation) for onboarding and project cohesion 📝

<a id="environment-setup-"></a>

# Environment setup [`⇧`](#contents)

1. First and foremost, please see the suggested IDE setup in the dropdown below to make sure that your editor is ready for development.

> [!IMPORTANT]
>
> <details><summary>Suggested IDE setup</summary>
>
> <p>
>
> VS Code
>
> Install the following extensions:
>
> - [charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
> - [streetsidesoftware.code-spell-checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
>
> </p>
> </details>

2. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the [ts-backend-check repo](https://github.com/activist-org/ts-backend-check), clone your fork, and configure the remotes:

> [!NOTE]
>
> <details><summary>Consider using SSH</summary>
>
> <p>
>
> Alternatively to using HTTPS as in the instructions below, consider SSH to interact with GitHub from the terminal. SSH allows you to connect without a user-pass authentication flow.
>
> To run git commands with SSH, remember then to substitute the HTTPS URL, `https://github.com/...`, with the SSH one, `git@github.com:...`.
>
> - e.g. Cloning now becomes `git clone git@github.com:<your-username>/ts-backend-check.git`
>
> GitHub also has their documentation on how to [Generate a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) 🔑
>
> </p>
> </details>

```bash
# Clone your fork of the repo into the current directory.
git clone https://github.com/<your-username>/ts-backend-check.git
# Navigate to the newly cloned directory.
cd ts-backend-check
# Assign the original repo to a remote called "upstream".
git remote add upstream https://github.com/activist-org/ts-backend-check.git
```

- Now, if you run `git remote -v` you should see two remote repositories named:
  - `origin` (forked repository)
  - `upstream` (ts-backend-check repository)

3. Install `uv` if you don't already have it by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

4. Create a virtual environment for ts-backend-check (Python `>=3.12`), activate it and install dependencies:

   ```bash
   uv sync --all-extras  # create .venv and install all dependencies from uv.lock

   # Unix or macOS:
   source .venv/bin/activate

   # Windows:
   .venv\Scripts\activate.bat  # .venv\Scripts\activate.ps1 (PowerShell)
   ```

> [!NOTE]
> If you change dependencies in `pyproject.toml`, regenerate the lock file with the following command:
>
> ```bash
> uv lock  # refresh uv.lock for reproducible installs
> ```

After activating the virtual environment, set up [pre-commit](https://pre-commit.com/) by running:

```bash
pre-commit install
# uv run pre-commit run --all-files  # lint and fix common problems in the codebase
```

You're now ready to work on `ts-backend-check`!

> [!NOTE]
> Feel free to contact the team in the [Development room on Matrix](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) if you're having problems getting your environment setup!

<a id="contributors"></a>

# Contributors [`⇧`](#contents)

Thanks to all our amazing [contributors](https://github.com/activist-org/ts-backend-check/graphs/contributors)! ❤️

<a href="https://github.com/activist-org/ts-backend-check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=activist-org/ts-backend-check" />
</a>
