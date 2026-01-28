================================
Contributing to ts-backend-check
================================

Thank you for contributing to ``ts-backend-check``!

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project. In return, and in accordance with this project's `code of conduct <https://github.com/activist-org/ts-backend-check/tree/main/.github/CODE_OF_CONDUCT.md>`_, other contributors will reciprocate that respect in addressing your issue or assessing patches and features.

If you have questions or would like to communicate with the team, please `join us in our public Matrix chat rooms <https://matrix.to/#/#activist_community:matrix.org>`_. We'd be happy to hear from you!

.. _contents:

**Contents**
------------

* :ref:`first-steps`
* :ref:`learning-the-tech-stack`
* :ref:`dev-env`
* :ref:`linting`
* :ref:`testing`
* :ref:`issues-projects`
* :ref:`bug-reports`
* :ref:`feature-requests`
* :ref:`pull-requests`
* :ref:`documentation`

---

.. _first-steps:

First steps as a contributor `⇧ <#contents>`_
--------------------------------------------

Thank you for your interest in contributing to activist community projects! We look forward to welcoming you :) The following are some suggested steps for people interested in joining our community:

* Please join the `public Matrix chat <https://matrix.to/#/#activist_community:matrix.org>`_ to connect with the community.
    * `Matrix <https://matrix.org/>`_ is a network for secure, decentralized communication.
    * We'd suggest that you use the `Element <https://element.io/>`_ client and `Element X <https://element.io/app>`_ for a mobile app.
    * The `General <https://matrix.to/#/!uIGQUxlCnEzrPiRsRw:matrix.org?via=matrix.org&via=effektio.org&via=acter.global>`_ and `Development <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ channels would be great places to start!
    * Feel free to introduce yourself and tell us what your interests are if you're comfortable :)
* Consider joining our `bi-weekly developer sync <https://etherpad.wikimedia.org/p/activist-dev-sync>`_!

.. _learning-the-tech-stack:

Learning the tech stack `⇧ <#contents>`_
----------------------------------------

``ts-backend-check`` is very open to contributions from people in the early stages of their coding journey! The following is a select list of documentation pages to help you understand the technologies we use.

**Docs for those new to programming**
    * `Mozilla Developer Network Learning Area <https://developer.mozilla.org/en-US/docs/Learn>`_
    * `Open Source Guides <https://opensource.guide/>`_

**Python learning docs**
    * `Python getting started guide <https://docs.python.org/3/tutorial/introduction.html>`_
    * `Python getting started resources <https://www.python.org/about/gettingstarted/>`_

.. _dev-env:

Development environment `⇧ <#contents>`_
----------------------------------------

1. First and foremost, please see the suggested IDE setup below to make sure that your editor is ready for development.

.. important::
   **Suggested IDE setup: VS Code**

   Install the following extensions:

   * `charliermarsh.ruff <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`_
   * `streetsidesoftware.code-spell-checker <https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker>`_

2. `Fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_ the `ts-backend-check repo <https://github.com/activist-org/ts-backend-check>`_, clone your fork, and configure the remotes:

.. note::
   **Consider using SSH**

   Alternatively to using HTTPS, consider SSH to interact with GitHub from the terminal.

   * e.g. Cloning becomes ``git clone git@github.com:<your-username>/ts-backend-check.git``
   * See GitHub's guide on `Generating a new SSH key <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_ 🔑

.. code-block:: bash

    # Clone your fork of the repo into the current directory.
    git clone https://github.com/<your-username>/ts-backend-check.git
    # Navigate to the newly cloned directory.
    cd ts-backend-check
    # Assign the original repo to a remote called "upstream".
    git remote add upstream https://github.com/activist-org/ts-backend-check.git

3. Create a virtual environment for ts-backend-check (Python ``>=3.12``), activate it and install dependencies:

.. note::
   First, install ``uv`` if you don't already have it by following the `official installation guide <https://docs.astral.sh/uv/getting-started/installation/>`_.

.. code-block:: bash

    uv sync --all-extras  # create .venv and install all dependencies from uv.lock

    # Unix or macOS:
    source .venv/bin/activate

    # Windows:
    .venv\Scripts\activate.bat # .venv\Scripts\activate.ps1 (PowerShell)

.. note::
   If you change dependencies in ``pyproject.toml``, regenerate the lock file with:

   .. code-block:: bash

      uv lock

After activating the virtual environment, set up `pre-commit <https://pre-commit.com/>`_ by running:

.. code-block:: bash

    pre-commit install

.. note::
   Feel free to contact the team in the `Development room on Matrix <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ if you're having problems!

.. _linting:

Linting `⇧ <#contents>`_
------------------------

`Ruff <https://github.com/astral-sh/ruff>`_ is installed via the required packages to assure that errors are reported correctly.

.. _testing:

Testing `⇧ <#contents>`_
------------------------

Please run the following commands from the project root to test:

.. code-block:: bash

    # Format, lint, and static type check:
    ruff format ./src
    ruff check ./src
    mypy ./src --config-file ./pyproject.toml

    # Run tests:
    pytest

    # Run with a coverage report:
    pytest . --cov=src --cov-report=term-missing --cov-config=./pyproject.toml

.. _issues-projects:

Issues and projects `⇧ <#contents>`_
------------------------------------

The `issue tracker for ts-backend-check <https://github.com/activist-org/ts-backend-check/issues>`_ is the preferred channel for bug reports and feature requests.

.. _bug-reports:

Bug reports `⇧ <#contents>`_
----------------------------

A bug is a *demonstrable problem* caused by the code.

1. **Search** existing issues.
2. **Reproduce** using the latest ``main``.
3. **Isolate** the problem.

Please report bugs using the `bug report template <https://github.com/activist-org/ts-backend-check/issues/new?assignees=&labels=bug&projects=activist-org%2F1&template=bug_report.yml>`_.

.. _feature-requests:

Feature requests `⇧ <#contents>`_
---------------------------------

Feature requests are more than welcome! Provide as much detail and context as possible.

.. _pull-requests:

Pull requests `⇧ <#contents>`_
------------------------------

Good pull requests should remain focused in scope. All contributions are made under the project's license.

**Please ask first** before embarking on any significant refactor or new feature. Adhering to the `GitHub flow <https://docs.github.com/en/get-started/quickstart/github-flow>`_ process is the best way to get your work merged.



1. **Sync your fork**:

   .. code-block:: bash

      git checkout <dev-branch>
      git pull upstream <dev-branch>

2. **Create a topic branch**:

   .. code-block:: bash

      git checkout -b <topic-branch-name>

3. **Install pre-commit**:

   .. code-block:: bash

      pre-commit install
      pre-commit run --all-files

.. note::
   If you have issues with pre-commit, you can bypass it with ``git commit --no-verify -m "MESSAGE"``.

4. **Commit logical chunks** using `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_.

5. **Merge/Rebase upstream**:

   .. code-block:: bash

      git pull --rebase upstream <dev-branch>

6. **Push and Open a Pull Request**.

.. _documentation:

Documentation `⇧ <#contents>`_
------------------------------

Documentation for ``ts-backend-check`` is hosted at `ts-backend-check.readthedocs.io <https://ts-backend-check.readthedocs.io/en/latest/>`_.

Function Docstrings
~~~~~~~~~~~~~~~~~~~

We follow `numpydoc conventions <https://numpydoc.readthedocs.io/en/latest/format.html>`_:

.. code-block:: py

    def example_function(argument: argument_type) -> return_type:
        """
        An example docstring for a function.

        Parameters
        ----------
        argument : argument_type
            Description of your argument.

        Returns
        -------
        return_value : return_type
            Description of your return value.

        Raises
        ------
        ErrorType
            Description of the condition that raises it.
        """
        ...
        return return_value

Building the Docs
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd docs
    make html
