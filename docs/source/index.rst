.. image:: https://raw.githubusercontent.com/activist-org/ts-backend-check/main/.github/resources/TSBackendCheckGitHubBanner.png
    :width: 100%
    :align: center
    :target: https://github.com/activist-org/ts-backend-check

|rtd| |ci_backend| |issues| |language| |pypi| |pypistatus| |license| |coc| |matrix|

.. |rtd| image:: https://img.shields.io/readthedocs/ts-backend-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff
    :target: http://ts-backend-check.readthedocs.io/en/latest/

.. |ci_backend| image:: https://img.shields.io/github/actions/workflow/status/activist-org/ts-backend-check/pr_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff
    :target: https://github.com/activist-org/ts-backend-check/actions/workflows/pr_ci_backend.yaml

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

**Check TypeScript types against backend models**

Installation
============

``ts-backend-check`` is available for installation via `pip <https://pypi.org/project/ts-backend-check/>`_:

.. code-block:: shell

    pip install ts-backend-check

The latest development version can further be installed the `source code on GitHub <https://github.com/activist-org/ts-backend-check>`_:

.. code-block:: shell

    git clone https://github.com/activist-org/ts-backend-check.git
    cd ts-backend-check
    pip install -e .

To utilize the ts-backend-check CLI, you can execute variations of the following command in your terminal:

.. code-block:: shell

    ts-backend-check -h  # view the cli options
    ts-backend-check [command]

Commands
========

The CLI provides a simple interface to check TypeScript types against backend models:

.. code-block:: shell

    # Show help and available commands:
    ts-backend-check --help

    # Check a TypeScript type against a backend model:
    ts-backend-check check <typescript-file> <backend-model-file>

    # Example command:
    ts-backend-check check src/types/user.ts src/models/user.py

Command Options
===============

- ``check``: Compare TypeScript types with backend models
    - ``typescript-file``: Path to the TypeScript interface/type file
    - ``backend-model-file``: Path to the backend model file (e.g. Python class)

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
