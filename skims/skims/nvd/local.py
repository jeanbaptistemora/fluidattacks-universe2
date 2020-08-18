# Standard library
from contextlib import (
    suppress,
)
from typing import (
    Dict,
    List,
)

# Third party libraries
from semver import (
    match,
)

# Constants
DATABASE: Dict[str, Dict[str, List[List[str]]]] = {
    'hoek': {
        'CVE-2018-3728': [
            ['>=0.0.0', '<4.2.0'],
            ['>=5.0.0', '<5.0.3'],
        ],
    },
    'jquery': {
        'CVE-2020-11022': [
            ['>=1.2.0', '<3.5.0'],
        ],
        'CVE-2020-7656': [
            ['<1.9.0'],
        ],
        'CVE-2019-11358': [
            ['<3.4.0'],
        ],
        'CVE-2019-5428': [
            ['<3.4.0'],
        ],
        'CVE-2017-16012': [
            ['<3.0.0'],
        ],
        'CVE-2017-16011': [
            ['>=1.7.1', '<1.9.0'],
        ],
        'CVE-2015-9251': [
            ['<3.0.0'],
        ],
        'CVE-2014-6071': [
            ['=1.4.2'],
        ],
        'CVE-2012-6708': [
            ['>=1.7.1', '<1.9.0'],
        ],
        'CVE-2011-4969': [
            ['<1.6.3'],
        ],
    },
}
"""Dictionary mapping products to their manually verified list of CVE."""

IGNORED_CHARS = str.maketrans('', '', ''.join({'^', '~'}))


def does_version_match(version: str, condition: str) -> bool:
    """Given a version and a condition return True if version match condition.
    """
    with suppress(ValueError):
        return match(version, condition)
    return False


def remove_constraints(version: str) -> str:
    """Remove version constrans like `^`, `~` and `*`.

    These version constraints may be resolved to the latest or may not.
    It's better not to assume things and go conservative.
    """
    return version.translate(IGNORED_CHARS).replace('.*', '.0')


def query(product: str, version: str) -> List[str]:
    """Search a product and a version in the database and return a list of CVE.
    """
    version = remove_constraints(version)

    cves: List[str] = [
        cve
        for cve, weak_versions in DATABASE.get(product.lower(), {}).items()
        for conditions in weak_versions
        if all(
            does_version_match(version, condition) for condition in conditions
        )
    ]

    return cves
