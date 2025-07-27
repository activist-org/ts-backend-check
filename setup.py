# SPDX-License-Identifier: GPL-3.0-or-later
import os

try:
    from setuptools import find_packages, setup

except ImportError:
    from distutils.core import setup

package_directory = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(package_directory, "requirements.txt"), encoding="utf-8"
) as req_file:
    requirements = req_file.readlines()

on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    requirements = []

setup_args = dict(
    name="ts-backend-check",
    version="1.1.0",
    package_dir={"": "src"},
    author="ts-backend-check developers",
    author_email="team@activist.org",
    description="Check TypeScript types against their corresponding backend models to assure that all fields have been accounted for.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/activist-org/ts-backend-check",
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "ts-backend-check=ts_backend_check.cli.main:main",
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

if __name__ == "__main__":
    setup(**setup_args)
