# Standard library
from contextlib import (
    suppress,
)
from sys import (
    modules,
)
from typing import (
    Dict,
    List,
    Literal,
)

# Third party libraries
from semver import (
    match,
)

# Constants
DATABASE_NPM: Dict[str, Dict[str, List[List[str]]]] = {
    'axioss': {
        'SNYK-JS-AXIOSS-460538': [
            ['>0.0.0'],
        ],
    },
    'axios-http': {
        'SNYK-JS-AXIOSHTTP-460539': [
            ['>0.0.0'],
        ],
    },
    'axios': {
        'CVE-2019-10742': [
            ['<=0.18.0'],
        ],
    },
    'bootstrap': {
        'CVE-2019-8331': [
            ['<3.4.1'],
            ['>=4.0.0', '<4.3.1'],
        ],
        'CVE-2018-20677': [
            ['<3.4.0'],
        ],
        'CVE-2018-20676': [
            ['<3.4.0'],
        ],
        'CVE-2018-14042': [
            ['<4.1.2'],
        ],
        'CVE-2018-14041': [
            ['<4.1.2'],
        ],
        'CVE-2018-14040': [
            ['<4.1.2'],
        ],
        'CVE-2016-10735': [
            ['<3.4.0'],
            ['>=4.0.0-alpha', '<4.0.0-beta.2'],
        ],
    },
    'debug': {
        'CVE-2017-16137': [
            ['>=1.0.0', '<2.6.9'],
            ['>=3.0.0', '<3.1.0'],
        ],
    },
    'elliptic': {
        'CVE-2020-13822': [
            ['<6.5.3'],
        ],
        'SNYK-JS-ELLIPTIC-511941': [
            ['<6.5.2'],
        ],
    },
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
    'lodahs': {
        'CVE-2019-19771': [
            ['>0.0.0'],
        ],
    },
    'lodash': {
        'CVE-2020-8203': [
            ['<=4.17.15'],
        ],
        'CVE-2019-1010266': [
            ['<4.17.11'],
        ],
        'CVE-2019-10744': [
            ['<4.17.12'],
        ],
        'CVE-2018-16487': [
            ['<4.17.11'],
        ],
        'CVE-2018-3721': [
            ['<4.17.5'],
        ],
        'SNYK-JS-LODASH-590103': [
            ['<4.17.20'],
        ],
    },
    'serialize-javascript': {
        'CVE-2020-7660': [
            ['<3.1.0'],
        ],
        'CVE-2019-16769': [
            ['<2.1.1'],
        ],
    },
    'set-value': {
        'CVE-2019-10747': [
            ['<3.0.1'],
        ],
    },
    'sockjs': {
        'CVE-2020-8823': [
            ['<0.3.0'],
        ],
        'CVE-2020-7693': [
            ['<0.3.20'],
        ],
    },
    'timespan': {
        'CVE-2017-16115': [
            ['>0.0.0', '<=2.3.0'],
        ],
    },
    'websocket-extensions': {
        'CVE-2020-7662': [
            ['<0.1.4'],
        ],
    },
    'yargs-parser': {
        'CVE-2020-7608': [
            ['<13.1.2'],
            ['>=14.0.0', '<15.0.1'],
            ['>=16.0.0', '<18.1.1'],
        ],
    },
}
"""Dictionary mapping products to their manually verified list of CVE."""

DATABASE_MAVEN: Dict[str, Dict[str, List[List[str]]]] = {
}
"""Dictionary mapping products to their manually verified list of CVE."""

IGNORED_CHARS = str.maketrans('', '', ''.join({'^', '~'}))


def does_version_match(version: str, condition: str) -> bool:
    """Given a version and a condition return True if version match condition.
    """
    with suppress(ValueError):
        return match(version, condition)
    return False


def normalize(version: str) -> str:
    """Normalize a version so it contains major. minor and patch."""
    while version.count('.') < 2:
        version += '.0'
    return version


def remove_constraints(version: str) -> str:
    """Remove version constrans like `^`, `~` and `*`.

    These version constraints may be resolved to the latest or may not.
    It's better not to assume things and go conservative.
    """
    return version.translate(IGNORED_CHARS).replace('.*', '.0')


def query(
    platform: Literal['NPM', 'MAVEN'],
    product: str,
    version: str,
) -> List[str]:
    """Search a product and a version in the database and return a list of CVE.
    """
    version = normalize(remove_constraints(version))
    database = getattr(modules[__name__], f'DATABASE_{platform}')

    cves: List[str] = [
        cve
        for cve, weak_versions in database.get(product.lower(), {}).items()
        for conditions in weak_versions
        if all(
            does_version_match(version, condition) for condition in conditions
        )
    ]

    return cves
