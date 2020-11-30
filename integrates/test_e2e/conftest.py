# Standard libraries
import os
from typing import Dict

# Third party libraries
import pytest

# Browserstack settings
BROWSERSTACK_USER: str = os.environ['BROWSERSTACK_USER']
BROWSERSTACK_KEY: str = os.environ['BROWSERSTACK_KEY']
BROWSERSTACK_URL: str = f'https://{BROWSERSTACK_USER}:{BROWSERSTACK_KEY}@hub-cloud.browserstack.com/wd/hub'
BROWSERSTACK_DESIRED_CAP: Dict[str, str] = {
    'os': 'Windows',
    'os_version': '10',
    'browser': 'Chrome',
    'browser_version': '80',
}

# Environment variables
BRANCH: str = os.environ['CI_COMMIT_REF_NAME']
CI: bool = bool(os.environ['CI'])

# Other variables
URL: str = ''
if BRANCH == 'master':
    URL = 'https://integrates.fluidattacks.com/new'
elif CI:
    URL = f'https://{BRANCH}.integrates.fluidattacks.com/new'
else:
    URL = 'https://localhost:8080/new'
