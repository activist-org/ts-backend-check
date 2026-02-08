.. image:: https://raw.githubusercontent.com/activist-org/ts-backend-check/main/.github/resources/TSBackendCheckGitHubBanner.png
    :width: 100%
    :align: center
    :target: https://github.com/activist-org/ts-backend-check

|rtd| |pr_ci| |python_package_ci| |issues| |language| |pypi| |pypistatus| |license| |coc| |matrix|

.. |rtd| image:: https://img.shields.io/readthedocs/ts-backend-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff
    :target: http://ts-backend-check.readthedocs.io/en/latest/

.. |pr_ci| image:: https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/pr_ci.yaml?branch=main&label=%20&logo=ruff&logoColor=ffffff
    :target: https://github.com/activist-org/ts-backend-check/actions/workflows/pr_ci.yaml

.. |python_package_ci| image:: https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/python_package_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff
    :target: https://github.com/activist-org/ts-backend-check/actions/workflows/python_package_ci.yaml

.. |issues| image:: https://img.shields.io/github/issues/activist-org/ts-backend-check?label=%20&logo=github
    :target: https://github.com/activist-org/ts-backend-check/issues

.. |language| image:: https://img.shields.io/badge/Python%203-306998.svg?logo=python&logoColor=ffffff
    :target: https://github.com/activist-org/ts-backend-check/blob/main/CONTRIBUTING.md

.. |pypi| image:: https://img.shields.io/pypi/v/ts-backend-check.svg?label=%20&color=4B8BBE
    :target: https://pypi.org/project/ts-backend-check/

.. |pypistatus| image:: https://img.shields.io/pypi/status/ts-backend-check.svg?label=%20
    :target: https://pypi.org/project/ts-backend-check/

.. |license| image:: https://img.shields.io/github/license/activist-org/ts-backend-check.svg?label=%20
    :target: https://github.com/activist-org/ts-backend-check/blob/main/LICENSE.txt

.. |coc| image:: https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg
    :target: https://github.com/activist-org/ts-backend-check/blob/main/.github/CODE_OF_CONDUCT.md

.. |matrix| image:: https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff
    :target: https://matrix.to/#/#activist_community:matrix.org

**Check TypeScript interfaces against backend models**

Installation
============

``ts-backend-check`` is available for installation via `uv <https://docs.astral.sh/uv/>`_ or `pip <https://pypi.org/project/ts-backend-check/>`_:

.. code-block:: shell

    # Using uv (recommended - fast, Rust-based installer):
    uv pip install ts-backend-check

    # Or using pip:
    pip install ts-backend-check

The latest development version can further be installed the `source code on GitHub <https://github.com/activist-org/ts-backend-check>`_:

.. code-block:: shell

    git clone https://github.com/activist-org/ts-backend-check.git
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

Command Options
===============

The CLI provides a simple interface to check TypeScript types against backend models:

.. code-block:: shell

    # Show help and available commands:
    ts-backend-check -h
    ts-backend-check -gcf  # generate a configuration file
    ts-backend-check -gtp  # generate a test project for experimenting with the CLI

    # Check a TypeScript type against a backend model:
    ts-backend-check -m <model-identifier-from-config-file>
    ts-backend-check -a  # run all models

Outputs
=======

Example success and error outputs for the CLI are:

.. code-block::

    ts-backend-check -m user
    ✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided files.

.. code-block::

    ts-backend-check -m user

    ❌ ts-backend-check error: There are inconsistencies between the provided backend models and TypeScript interfaces. Please see the output below for details.

    Field 'user_name' (camelCase: 'userName') from model 'UserModel' is missing in the TypeScript interfaces.
    Expected to find this field in the frontend interface: User
    To ignore this field, add the following comment to the TypeScript interface: '// ts-backend-check: ignore userName'

    Please fix the 1 error above to have the backend models of backend/models/user.py synced with the TypeScript interfaces of frontend/types/user.ts.

Contents
========

.. toctree::
    :maxdepth: 2

    ts_backend_check/index

Contributing
============

.. toctree::
    :maxdepth: 2

    notes

Project Indices
===============

* :ref:`genindex`
