================================
Contributing to ts-backend-check
================================

Thank you for contributing to ``ts-backend-check``!

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project. In return, and in accordance with this project's `code of conduct <https://github.com/activist-org/ts-backend-check/tree/main/.github/CODE_OF_CONDUCT.md>`_, other contributors will reciprocate that respect in addressing your issue or assessing patches and features.

If you have questions or would like to communicate with the team, please `join us in our public Matrix chat rooms <https://matrix.to/#/#activist_community:matrix.org>`_. We'd be happy to hear from you!

.. _contents:

Contents
--------

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

.. _first-steps:

First steps as a contributor `⇧ <#contents>`_
---------------------------------------------

Thank you for your interest in contributing to activist community projects! We look forward to welcoming you :) The following are some suggested steps for people interested in joining our community:

* Please join the `public Matrix chat <https://matrix.to/#/#activist_community:matrix.org>`_ to connect with the community
    * `Matrix <https://matrix.org/>`_ is a network for secure, decentralized communication
    * We'd suggest that you use the `Element <https://element.io/>`_ client and `Element X <https://element.io/app>`_ for a mobile app
    * The `General <https://matrix.to/#/!uIGQUxlCnEzrPiRsRw:matrix.org?via=matrix.org&via=effektio.org&via=acter.global>`_ and `Development <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ channels would be great places to start!
    * Feel free to introduce yourself and tell us what your interests are if you're comfortable :)
* Consider joining our `bi-weekly developer sync <https://etherpad.wikimedia.org/p/activist-dev-sync>`_!

.. _learning-the-tech-stack:

Learning the tech stack `⇧ <#contents>`_
----------------------------------------

``ts-backend-check`` is very open to contributions from people in the early stages of their coding journey! The following is a select list of documentation pages to help you understand the technologies we use.

Docs for those new to programming
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Mozilla Developer Network Learning Area <https://developer.mozilla.org/en-US/docs/Learn>`_
    * Doing MDN sections for HTML, CSS and JavaScript is the best ways to get into web development!
* `Open Source Guides <https://opensource.guide/>`_
    * Guides from GitHub about open-source software including how to start and much more!

Python learning docs
~~~~~~~~~~~~~~~~~~~~

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

    Alternatively to using HTTPS, consider SSH to interact with GitHub from the terminal. SSH allows you to connect without a user-pass authentication flow.

    To run git commands with SSH, substitute the HTTPS URL with the SSH one: ``git@github.com:...``.

    GitHub also has documentation on how to `Generate a new SSH key <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_ 🔑

.. code-block:: bash

    # Clone your fork of the repo into the current directory.
    git clone https://github.com/<your-username>/ts-backend-check.git
    # Navigate to the newly cloned directory.
    cd ts-backend-check
    # Assign the original repo to a remote called "upstream".
    git remote add upstream https://github.com/activist-org/ts-backend-check.git

* Now, if you run ``git remote -v`` you should see two remote repositories named:
    * ``origin`` (forked repository)
    * ``upstream`` (``ts-backend-check`` repository)

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

        uv lock  # refresh uv.lock for reproducible installs

After activating the virtual environment, set up `pre-commit <https://pre-commit.com/>`_ by running:

.. code-block:: bash

    pre-commit install
    # uv run pre-commit run --all-files

You're now ready to work on ``ts-backend-check``!

.. note::
    Feel free to contact the team in the `Development room on Matrix <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ if you're having problems!

.. _linting:

Linting `⇧ <#contents>`_
------------------------

`Ruff <https://github.com/astral-sh/ruff>`_ is installed via the required packages to assure that errors are reported correctly. We'd also suggest that VS Code users install the `Ruff extension <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`_.

.. _testing:

Testing `⇧ <#contents>`_
------------------------

Please run the following commands from the project root to test:

.. code-block:: bash

    # Format the src directory, lint the code and run static type checks:
    ruff format ./src
    ruff check ./src
    mypy ./src --config-file ./pyproject.toml

    # Run tests:
    pytest

    # To run a specific test:
    pytest path/to/test_file.py::test_function

    # To run with a coverage report as is done in PRs:
    pytest . --cov=src --cov-report=term-missing --cov-config=./pyproject.toml

.. _issues-projects:

Issues and projects `⇧ <#contents>`_
------------------------------------

The `issue tracker for ts-backend-check <https://github.com/activist-org/ts-backend-check/issues>`_ is the preferred channel for bug reports, features requests and submitting pull requests. The activist community also organizes related issues into `projects <https://github.com/activist-org/ts-backend-check/projects>`_.

.. _bug-reports:

Bug reports `⇧ <#contents>`_
----------------------------

A bug is a *demonstrable problem* that is caused by the code in the repository. Good bug reports are extremely helpful — thank you!

Guidelines for bug reports:

1. **Use the GitHub issue search** to check if the issue has already been reported.
2. **Check if the issue has been fixed** by trying to reproduce it using the latest ``main`` branch.
3. **Isolate the problem** to make sure the code in the repository is responsible.

**Great Bug Reports** tend to have:

* A quick summary
* Steps to reproduce
* What you expected would happen
* What actually happens
* Notes (why this might be happening, things tried, etc)

To make the above steps easier, use the `bug report template <https://github.com/activist-org/ts-backend-check/issues/new?assignees=&labels=bug&projects=activist-org%2F1&template=bug_report.yml>`_.

.. _feature-requests:

Feature requests `⇧ <#contents>`_
---------------------------------

Feature requests are more than welcome! When making a suggestion, provide as much detail and context as possible. Feature requests are marked with the `Feature <https://github.com/activist-org/ts-backend-check/issues?q=is%3Aissue%20state%3Aopen%20type%3AFeature>`_ type.

.. _pull-requests:

Pull requests `⇧ <#contents>`_
------------------------------

Good pull requests — patches, improvements and new features — are the foundation of our community. They should remain focused in scope. Note that all contributions will be made under `the specified license <LICENSE.txt>`_.

**Please ask first** before embarking on any significant pull request. Adhering to the `GitHub flow <https://docs.github.com/en/get-started/quickstart/github-flow>`_ process is the best way to get your work merged:



1. Get the latest changes from upstream:

   .. code-block:: bash

      git checkout <dev-branch>
      git pull upstream <dev-branch>

2. Create a new topic branch:

   .. code-block:: bash

      git checkout -b <topic-branch-name>

3. Install `pre-commit <https://pre-commit.com/>`_:

   .. code-block:: bash

      pre-commit install
      pre-commit run --all-files

4. Commit your changes in logical chunks, adhering to `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_.

5. Locally merge (or rebase) the upstream development branch:

   .. code-block:: bash

      git pull --rebase upstream <dev-branch>

6. Push your topic branch to your fork:

   .. code-block:: bash

      git push origin <topic-branch-name>

7. `Open a Pull Request <https://help.github.com/articles/using-pull-requests/>`_ with a clear title and description.

.. _documentation:

Documentation `⇧ <#contents>`_
------------------------------

The documentation for ``ts-backend-check`` can be found at `ts-backend-check.readthedocs.io <https://ts-backend-check.readthedocs.io/en/latest/>`_.

Function Docstrings
~~~~~~~~~~~~~~~~~~~

We follow `numpydoc conventions <https://numpydoc.readthedocs.io/en/latest/format.html>`_.

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

Open ``index.html`` within ``docs/build/html`` to check the local version.
