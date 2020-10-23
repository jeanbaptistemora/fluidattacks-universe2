# Standar libraries
import os
import re
from distutils.version import StrictVersion

# Third party libraries
import requests

# Local libraries
from toolbox.constants import PACKAGE_MANAGER, VERSION, CLI_NAME


def get_pypi_info():
    try:
        url = f"https://pypi.org/pypi/{CLI_NAME}/json"
        data = requests.get(url).json()
        return data
    except requests.exceptions.RequestException:
        return []


def get_versions() -> list:
    pipy_info = get_pypi_info()
    if not pipy_info:
        return [CLI_NAME]

    return sorted(list(pipy_info["releases"].keys()),
                  key=StrictVersion,
                  reverse=True)


def get_last_pypi_version() -> str:
    versions = get_versions()
    return versions[0]


def get_last_nix_hash() -> str:
    pypi_info = get_pypi_info()
    if pypi_info:
        package_description = pypi_info['info']['description']
        hash_search = re.match(r"nix_hash:([a-z0-9]{32})", package_description)

        if hash_search is None:
            return ""

        return hash_search.group(1)

    return ""


def check_new_version() -> bool:
    if PACKAGE_MANAGER == 'pip':
        return VERSION != get_last_pypi_version()

    last_nix_hash = get_last_nix_hash()
    return not os.path.exists(f"/nix/store/{last_nix_hash}-{CLI_NAME}")
