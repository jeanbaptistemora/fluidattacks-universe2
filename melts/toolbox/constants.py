# Standard library
import os
import re
import sys
from typing import Dict
import pkg_resources

# Constants
CLI_NAME = "melts"
BASE_DIR = os.path.dirname(__file__)
VERSION = pkg_resources.get_distribution(CLI_NAME).version

SAST: tuple = ('lines',)
DAST: tuple = ('inputs', 'ports',)
API_TOKEN: str = os.environ.get('INTEGRATES_API_TOKEN', '')
DATE_FORMAT: str = '%Y-%m-%dT%H:%M:%SZ'

RICH_EXIT_CODES: Dict[str, int] = {
    'closed': 0,
    'open': 101,
    'unknown': 102,

    'config-error': 78,

    'exploit-error': 103,
    'exploit-not-found': 104,
}
RICH_EXIT_CODES_INV: Dict[int, str] = {
    v: k for k, v in RICH_EXIT_CODES.items()}

LOGGER_DEBUG: bool = os.environ.get('LOGGER_DEBUG', 'false') == 'true'

# Validations
if not API_TOKEN:
    print('Please set INTEGRATES_API_TOKEN environment variable.')
    print('  You can generate one at https://integrates.fluidattacks.com')
    sys.exit(78)

EXP_LABELS = ('product-ch', 'product-ch', 'product-fn',
              'service-logic', 'toe-location', 'toe-resource', 'toe-unreach')
RE_EXPLOIT_REASON = re.compile(r'(?::\s*(?P<reason>[\w ]+))')
