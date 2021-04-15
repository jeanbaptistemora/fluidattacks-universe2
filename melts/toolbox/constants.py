# Standard library
import os
import sys

# Constants
BASE_DIR = os.path.dirname(__file__)

API_TOKEN: str = os.environ.get('INTEGRATES_API_TOKEN', '')

LOGGER_DEBUG: bool = os.environ.get('LOGGER_DEBUG', 'false') == 'true'

# Validations
if not API_TOKEN:
    print('Please set INTEGRATES_API_TOKEN environment variable.')
    print('  You can generate one at https://app.fluidattacks.com')
    sys.exit(78)
