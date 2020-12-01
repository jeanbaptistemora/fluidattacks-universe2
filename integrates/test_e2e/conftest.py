# Standard libraries
import os
from typing import Dict

# Third party libraries
import pytest


@pytest.fixture(autouse=True, scope='session')
def browserstack_url() -> str:
    user = os.environ['BROWSERSTACK_USER']
    key = os.environ['BROWSERSTACK_KEY']
    return f'https://{user}:{key}@hub-cloud.browserstack.com/wd/hub'


@pytest.fixture(autouse=True, scope='session')
def browserstack_cap() -> Dict[str, str]:
    return {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': '80',
    }


@pytest.fixture(autouse=True, scope='session')
def branch() -> str:
    return os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')
def is_ci() -> bool:
    return bool(os.environ['CI'])


@pytest.fixture(autouse=True, scope='session')
def endpoint(branch: str, is_ci: bool) -> str:
    url: str = ''
    if branch == 'master':
        url = 'https://integrates.fluidattacks.com/new'
    elif is_ci:
        url = f'https://{branch}.integrates.fluidattacks.com/new'
    else:
        url = 'https://localhost:8080/new'
    return url
