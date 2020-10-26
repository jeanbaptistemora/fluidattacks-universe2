# Standar libraries
import os
import re
from distutils.version import StrictVersion

# Third party libraries
import requests

# Local libraries
from toolbox import logger
from toolbox.constants import PACKAGE_MANAGER, VERSION, CLI_NAME
from toolbox.utils.generic import run_command, go_back_to_services


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


def upgrade() -> bool:
    if PACKAGE_MANAGER == 'pip':
        command = "pip install --upgrade --force-reinstall melts"
    else:
        go_back_to_services()
        command = "./install.sh"

    status, stdout, stderr = run_command(command.split(), cwd='.', env={})
    if status:
        logger.error('Static checker has failed, output:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False
    return True
