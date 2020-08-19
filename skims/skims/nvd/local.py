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
    'adm-zip': {
        'CVE-2018-1002204': [
            ['<0.4.9'],
        ],
    },
    'ajv': {
        'CVE-2020-15366': [
            ['<6.12.3'],
        ],
    },
    'atob': {
        'CVE-2018-3745': [
            ['<2.0.3'],
        ],
        'hackerone.com/reports/321686': [
            ['<2.1.0'],
        ],
    },
    'axioss': {
        'npmjs.com/advisories/1124': [
            ['>=0.0.0'],
        ],
    },
    'axios-http': {
        'npmjs.com/advisories/1123': [
            ['>=0.0.0'],
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
    'braces': {
        'npmjs.com/advisories/786': [
            ['<2.3.1'],
        ],
    },
    'chownr': {
        'CVE-2017-18869': [
            ['<1.1.0'],
        ],
    },
    'cryptiles': {
        'npmjs.com/advisories/720': [
            ['>=4.0.0', '<4.1.2'],
            ['>=3.1.0', '<3.1.3'],
        ],
        'CVE-2018-1000620': [
            ['>=4.0.0', '<4.1.2'],
        ],
    },
    'debug': {
        'CVE-2017-16137': [
            ['>=1.0.0', '<2.6.9'],
            ['>=3.0.0', '<3.1.0'],
        ],
    },
    'decamelize': {
        'CVE-2017-16023': [
            ['>=1.1.0', '<1.1.2'],
        ],
    },
    'decompress': {
        'github.com/kevva/decompress/issues/71': [
            ['<4.2.1'],
        ],
    },
    'decompress-tar': {
        'npmjs.com/advisories/1217': [
            ['4.2.1'],
        ],
    },
    'decompress-zip': {
        'npmjs.com/advisories/777': [
            ['<0.2.2'],
            ['>=0.3.0', '<0.3.2'],
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
    'extend': {
        'CVE-2018-16492': [
            ['<2.0.2'],
            ['>=3.0.0', '<3.0.2'],
        ],
    },
    'fresh': {
        'CVE-2017-16119': [
            ['<0.5.2'],
        ],
    },
    'handlebars': {
        'CVE-2015-8861': [
            ['<4.0.0'],
        ],
        'github.com/handlebars-lang/handlebars.js/issues/1558': [
            ['<3.8.0'],
            ['>=4.0.0', '<4.3.0'],
        ],
        'github.com/handlebars-lang/handlebars.js/issues/1495': [
            ['>=3.0.0', '<3.0.7'],
            ['>=4.0.0', '<4.0.14'],
            ['>=4.1.0', '<4.1.2'],
        ],
        'hackerone.com/reports/726364': [
            ['<4.6.0'],
        ],
        'npmjs.com/advisories/1325': [
            ['<3.0.8'],
            ['>=4.0.0', '<4.5.3'],
        ],
        'npmjs.com/advisories/1324': [
            ['<3.0.8'],
            ['>=4.0.0', '<4.5.3'],
        ],
        'npmjs.com/advisories/1316': [
            ['<3.0.8'],
            ['>=4.0.0', '<4.5.3'],
        ],
        'npmjs.com/advisories/1300': [
            ['<4.4.5'],
        ],
        'npmjs.com/advisories/755': [
            ['>=4.0.0', '<4.0.14'],
            ['>=4.1.0', '<4.1.2'],
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
            ['==1.4.2'],
        ],
        'CVE-2012-6708': [
            ['>=1.7.1', '<1.9.0'],
        ],
        'CVE-2011-4969': [
            ['<1.6.3'],
        ],
    },
    'kind-of': {
        'CVE-2019-20149': [
            ['>=6.0.0', '<6.0.3'],
        ],
    },
    'lodahs': {
        'CVE-2019-19771': [
            ['>=0.0.0'],
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
        'github.com/lodash/lodash/issues/4874': [
            ['<4.17.20'],
        ],
    },
    'mime': {
        'CVE-2017-16138': [
            ['<1.4.1'],
            ['>=2.0.0', '<2.0.3'],
        ],
    },
    'minimatch': {
        'CVE-2016-10540': [
            ['<=3.0.1'],
        ],
    },
    'minimist': {
        'CVE-2020-7598': [
            ['<=1.2.2'],
        ],
    },
    'mixin-deep': {
        'CVE-2019-10746': [
            ['>=2.0.0', '<2.0.1'],
            ['<1.3.2'],
        ],
        'CVE-2018-3719': [
            ['<1.3.1'],
        ],
    },
    'ms': {
        'CVE-2015-8315': [
            ['<0.7.1'],
        ],
        (
            'github.com/vercel/ms/pull/89/commits'
            '/305f2ddcd4eff7cc7c518aca6bb2b2d2daad8fef'
        ): [
            ['>=0.7.1', '<2.0.0'],
        ],
    },
    'parsejson': {
        'CVE-2017-16113': [
            ['<=0.0.3'],
        ],
    },
    'request': {
        'CVE-2017-16026': [
            ['>=2.2.6', '<2.47.0'],
            ['>2.51.0', '<=2.67.0'],
        ],
        'npmjs.com/advisories/309': [
            ['>2.2.5', '<2.68.0'],
        ],
    },
    'semver': {
        'CVE-2015-8855': [
            ['<4.3.2'],
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
    'superagent': {
        'CVE-2017-16129': [
            ['<3.7.0'],
        ],
        'github.com/visionmedia/superagent/issues/1309': [
            ['<3.8.1'],
        ],
        'npmjs.com/advisories/479': [
            ['<3.7.0'],
        ],
    },
    'timespan': {
        'CVE-2017-16115': [
            ['>=0.0.0', '<=2.3.0'],
        ],
    },
    'tough-cookie': {
        'CVE-2017-15010': [
            ['<2.3.3'],
        ],
        'CVE-2016-1000232': [
            ['>=0.9.7', '<2.3.0'],
        ],
        'github.com/salesforce/tough-cookie/issues/92': [
            ['<2.3.3'],
        ],
    },
    'treekill': {
        'CVE-2019-15598': [
            ['<1.0.0'],
        ],
        'hackerone.com/reports/703415': [
            ['<1.0.0'],
        ],
    },
    'tree-kill': {
        'CVE-2019-15599': [
            ['<1.2.2'],
        ],
        'hackerone.com/reports/701183': [
            ['<1.2.2'],
        ],
    },
    'webpack-dev-server': {
        'CVE-2018-14732': [
            ['<3.1.6'],
        ],
        'github.com/webpack/webpack-dev-server/issues/1445': [
            ['>=2.0.0', '<2.11.4'],
            ['>=3.0.0', '<3.1.11'],
        ],
        'npmjs.com/advisories/725': [
            ['>=2.0.0', '<2.11.4'],
            ['>=3.0.0', '<3.1.11'],
        ],
    },
    'websocket-extensions': {
        'CVE-2020-7662': [
            ['<0.1.4'],
        ],
    },
    'yargs-parser': {
        'CVE-2020-7608': [
            ['!=5.0.0-security.0', '<13.1.2'],
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
    """Normalize a version so it contains major, minor and patch."""
    while version.count('.') < 2:
        version += '.0'
    return version


def remove_constraints(version: str) -> str:
    """Remove version constrans like `^`, `~` and `*`.

    These version constraints may be resolved to the latest or may not.
    It's better not to assume things and go conservative.
    """
    if version == '*':
        return '0'

    return version \
        .translate(IGNORED_CHARS) \
        .replace('.*', '.0') \
        .replace('.x', '.0') \



def query(
    platform: Literal['NPM', 'MAVEN'],
    product: str,
    version: str,
) -> List[str]:
    """Search a product and a version in the database and return a list of CVE.
    """
    version = normalize(remove_constraints(version.strip().lower()))
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
