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
}
IGNORED_CHARS = str.maketrans('', '', ''.join({'^', '~'}))


def does_version_match(version: str, condition: str) -> bool:
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
