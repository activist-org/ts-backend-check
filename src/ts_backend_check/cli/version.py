# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functions for checking current version of the ts-backend-check CLI.
"""

import importlib.metadata
from typing import Any, Dict

import requests

UNKNOWN_VERSION = "Unknown ts-backend-check version"
UNKNOWN_VERSION_NOT_PIP = f"{UNKNOWN_VERSION} (Not installed via pip)"
UNKNOWN_VERSION_NOT_FETCHED = f"{UNKNOWN_VERSION} (Unable to fetch version)"


def get_local_version() -> str:
    """
    Get the local version of the ts-backend-check package.

    Returns
    -------
    str
        The version of the installed ts-backend-check package, or a message indicating
        that the package is not installed via pip.
    """
    try:
        return importlib.metadata.version("ts-backend-check")

    except importlib.metadata.PackageNotFoundError:
        return UNKNOWN_VERSION_NOT_PIP


def get_latest_version() -> Any:
    """
    Get the latest version of the ts-backend-check package from GitHub.

    Returns
    -------
    Any
        The latest version of the ts-backend-check package, or a message indicating
        that the version could not be fetched.
    """
    try:
        response = requests.get(
            "https://api.github.com/repos/activist-org/ts-backend-check/releases/latest"
        )
        response_data: Dict[str, Any] = response.json()
        return response_data["name"]

    except Exception:
        return UNKNOWN_VERSION_NOT_FETCHED


def get_version_message() -> str:
    """
    Get a message indicating the local and latest versions of the ts-backend-check package.

    Returns
    -------
    str
        A message indicating the local version, the latest version, and whether
        an upgrade is available.
    """
    local_version = get_local_version()
    latest_version = get_latest_version()

    if local_version == UNKNOWN_VERSION_NOT_PIP:
        return UNKNOWN_VERSION_NOT_PIP

    elif latest_version == UNKNOWN_VERSION_NOT_FETCHED:
        return UNKNOWN_VERSION_NOT_FETCHED

    local_version_clean = local_version.strip()
    latest_version_clean = latest_version.replace("ts-backend-check", "").strip()

    if local_version_clean == latest_version_clean:
        return f"ts-backend-check v{local_version_clean}"

    elif local_version_clean > latest_version_clean:
        return f"ts-backend-check v{local_version_clean} is higher than the currently released version ts-backend-check v{latest_version_clean}. Hopefully this is a development build, and if so, thanks for your work on ts-backend-check! If not, please report this to the team at https://github.com/activist-org/ts-backend-check/issues."

    else:
        return f"ts-backend-check v{local_version_clean} (Upgrade available: ts-backend-check v{latest_version_clean}). To upgrade: ts-backend-check -u"


if __name__ == "__main__":
    print(get_version_message())
