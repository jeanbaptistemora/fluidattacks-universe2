# Standard libraries
import re
from typing import (
    List,
    Tuple,
)

# Third-party libraries
import requests
from pkg_resources import (
    get_distribution,
    DistributionNotFound,
)
from requests.exceptions import RequestException

# Local libraries
from utils.logs import (
    log,
    log_exception,
)


# Constants
PKG_NAME: str = 'sorts'
PYPI_URL: str = f'https://pypi.org/project/{PKG_NAME}/'
VERSION_REGEX = re.compile(r'{} [0-9\.]+'.format(PKG_NAME))


def check_version_is_latest() -> bool:
    """Checks whether the installed version is the latest listed on PyPI"""
    is_version_latest: bool = True
    try:
        current_version: Tuple[int, ...] = get_current()
        latest_version: Tuple[int, ...] = get_latest()
        log(
            'info',
            f"Current version: {'.'.join([str(x) for x in current_version])}\t"
            f"Latest version: {'.'.join([str(x) for x in latest_version])}"
        )
        if is_version_higher(latest_version, current_version):
            is_version_latest = False
    except (
        DistributionNotFound,
        RequestException,
    ):
        log(
            'info',
            'It was not possible to check if the latest version is installed'
        )
    return is_version_latest


def get_current() -> Tuple[int, ...]:
    """Get installed version of the package"""
    try:
        current = ver_to_tuple(get_distribution(PKG_NAME).version)
    except DistributionNotFound as exc:
        current = tuple()
        log_exception(
            'error',
            exc,
            message='Package cannot be found in the system'
        )
        raise exc
    return current


def get_latest() -> Tuple[int, ...]:
    """Get latest version indexed in PyPI"""
    latest: Tuple[int, ...] = tuple()
    try:
        with requests.Session() as session:
            response = session.get(PYPI_URL)
            if response.status_code == 200:
                version: List[str] = re.findall(VERSION_REGEX, response.text)
                latest = ver_to_tuple(version[0].split(' ')[1])
            else:
                log(
                    'error',
                    'The request to PyPI did not return 200. '
                    'Is the service available?'
                )
    except RequestException as exc:
        log_exception(
            'error',
            exc,
            message='There was an error fetching the latest version from PyPI'
        )
        raise exc
    return latest


def is_version_higher(ver1: Tuple[int, ...], ver2: Tuple[int, ...]) -> bool:
    """Checks if ver1 is higher than ver2"""
    is_higher: bool = False
    for idx, num in enumerate(ver1):
        if num > ver2[idx]:
            is_higher = True
            break
    return is_higher


def ver_to_tuple(value: str) -> Tuple[int, ...]:
    """Convert version like string to a tuple of integers"""
    return tuple(int(_f) for _f in re.split(r'\D+', value) if _f)
