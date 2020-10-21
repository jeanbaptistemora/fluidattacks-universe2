# Standar libraries
from distutils.version import StrictVersion

# Third party libraries
import requests

# Local libraries
from toolbox.constants import CLI_NAME


def get_versions() -> list:
    url = f"https://pypi.org/pypi/{CLI_NAME}/json"
    try:
        data = requests.get(url).json()
        return sorted(list(data["releases"].keys()),
                      key=StrictVersion,
                      reverse=True)
    except requests.exceptions.RequestException:
        return []


def get_last_version() -> str:
    versions = get_last_version()
    return versions[0]
