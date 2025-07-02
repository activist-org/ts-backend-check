<div align="center">
  <a href="https://github.com/activist-org/ts-backend-check"><img src="https://raw.githubusercontent.com/activist-org/ts-backend-check/main/.github/resources/TSBackendCheckGitHubBanner.png" width=1024 alt="TS Backend Check logo"></a>
</div>

[![rtd](https://img.shields.io/readthedocs/ts-backend-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff)](http://ts-backend-check.readthedocs.io/en/latest/)
[![ci_backend](https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/pr_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff)](https://github.com/activist-org/ts-backend-check/actions/workflows/pr_ci_backend.yaml)
[![issues](https://img.shields.io/github/issues/activist-org/ts-backend-check?label=%20&logo=github)](https://github.com/activist-org/ts-backend-check/issues)
[![python](https://img.shields.io/badge/Python-4B8BBE.svg?logo=python&logoColor=ffffff)](https://github.com/activist-org/ts-backend-check/blob/main/CONTRIBUTING.md)
[![pypi](https://img.shields.io/pypi/v/ts-backend-check.svg?label=%20&color=4B8BBE)](https://pypi.org/project/ts-backend-check/)
[![pypistatus](https://img.shields.io/pypi/status/ts-backend-check.svg?label=%20)](https://pypi.org/project/ts-backend-check/)
[![license](https://img.shields.io/github/license/activist-org/ts-backend-check.svg?label=%20)](https://github.com/activist-org/ts-backend-check/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg)](https://github.com/activist-org/ts-backend-check/blob/main/.github/CODE_OF_CONDUCT.md)
[![matrix](https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff)](https://matrix.to/#/#activist_community:matrix.org)

### Check TypeScript types against backend models

`ts-backend-check` is a Python package used to check TypeScript types against their corresponding backend models to assure that all fields have been accounted for.

<a id="contents"></a>

# **Contents**

- [Usage](#usage-)
- [Contributing](#contributing-)
- [Environment setup](#environment-setup)
- [Contributors](#contributors-)

<a id="usage"></a>

## Usage [`⇧`](#contents)

### Installation

```bash
pip install ts-backend-check
```

### Basic Usage

The CLI provides a simple interface to check TypeScript types against backend models:

```bash
# Show help and available commands:
ts-backend-check --help

# Check a TypeScript type against a backend model:
ts-backend-check check <typescript-file> <backend-model-file>

# Example command:
ts-backend-check check src/types/user.ts src/models/user.py
```

### Command Options

- `check`: Compare TypeScript types with backend models
  - `typescript-file`: Path to the TypeScript interface/type file
  - `backend-model-file`: Path to the backend model file (e.g. Python class)

### Version Information

```bash
ts-backend-check --version
```

<a id="contributing"></a>

# Contributing [`⇧`](#contents)

<a href="https://matrix.to/#/#activist_community:matrix.org"><img src="https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png" height="50" alt="Public Matrix Chat" align="right"></a>

activist uses [Matrix](https://matrix.org/) for internal communication. You're more than welcome to [join us in our public chat rooms](https://matrix.to/#/#activist_community:matrix.org) to share ideas, ask questions or just say hi to the team :)

Please see the [contribution guidelines](CONTRIBUTING.md) if you are interested in contributing. Work that is in progress or could be implemented is tracked in the [issues](https://github.com/activist-org/ts-backend-check/issues) and [projects](https://github.com/activist-org/ts-backend-check/projects).

> [!NOTE]
> Just because an issue is assigned on GitHub doesn't mean the team isn't open to your contribution! Feel free to write [in the issues](https://github.com/activist-org/ts-backend-check/issues) and we can potentially reassign it to you.

Also check the [`-next release-`](https://github.com/activist-org/ts-backend-check/labels/-next%20release-) and [`-priority-`](https://github.com/activist-org/ts-backend-check/labels/-priority-) labels in the [issues](https://github.com/activist-org/ts-backend-check/issues) for those that are most important, as well as those marked [`good first issue`](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) that are tailored for first-time contributors. For those new to coding or our tech stack, we've collected [links to helpful documentation pages](CONTRIBUTING.md#learning-the-tech-stack-) in the [contribution guidelines](CONTRIBUTING.md).

We would be happy to discuss granting you further rights as a contributor after your first pull requests, with a maintainer role then being possible after continued interest in the project. activist seeks to be an inclusive, diverse and supportive organization. We'd love to have you on the team!

<a id="how-you-can-help"></a>

## How you can help [`⇧`](#contents)

- [Reporting bugs](https://github.com/activist-org/ts-backend-check/issues/new?assignees=&labels=bug&template=bug_report.yml) as they're found 🐞
- Working with us on [new features](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3Afeature) ✨
- [Documentation](https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation) for onboarding and project cohesion 📝

<a id="environment-setup"></a>

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

3. Create a virtual environment, activate it and install dependencies:

   ```bash
   # Unix or MacOS:
   python3 -m venv venv
   source venv/bin/activate

   # Windows:
   python -m venv venv
   venv\Scripts\activate.bat

   # After activating venv:
   pip install --upgrade pip
   pip install -r requirements-dev.txt

   # To install the CLI for local development:
   pip install -e .
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
