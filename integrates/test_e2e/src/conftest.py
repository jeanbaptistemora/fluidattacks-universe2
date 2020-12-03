# Standard libraries
import os
from typing import Dict

# Third party libraries
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver import Firefox, Remote
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options


@pytest.fixture(autouse=True, scope='session')
def browserstack_url() -> str:
    user: str = os.environ['BROWSERSTACK_USER']
    key: str = os.environ['BROWSERSTACK_KEY']
    return f'https://{user}:{key}@hub-cloud.browserstack.com/wd/hub'


@pytest.fixture(autouse=True, scope='function')
def browserstack_cap(request: FixtureRequest) -> Dict[str, str]:
    return {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': '80',
        'name': request.node.name,
    }


@pytest.fixture(autouse=True, scope='session')
def branch() -> str:
    return os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')
def is_ci() -> bool:
    return bool(os.environ['CI'])


@pytest.fixture(autouse=True, scope='session')
def azure_credentials() -> Dict[str, str]:
    user: str = os.environ['TEST_E2E_AZURE_USER']
    password: str = os.environ['TEST_E2E_AZURE_PASS']
    seed: str = os.environ['TEST_E2E_AZURE_SEED']
    return {
        'user': user,
        'password': password,
        'seed': seed,
    }


@pytest.fixture(autouse=True, scope='session')
def endpoint(branch: str, is_ci: bool) -> str:
    url: str = ''
    if branch == 'master':
        url = 'https://integrates.fluidattacks.com/new'
    elif is_ci:
        url = f'https://{branch}.integrates.fluidattacks.com/new'
    else:
        url = 'https://localhost:8081/new'
    return url


@pytest.fixture(autouse=True, scope='function')
def driver(
        browserstack_cap: Dict[str, str],
        browserstack_url: str,
        is_ci: bool) -> WebDriver:
    driver: WebDriver = None
    if is_ci:
        driver = Remote(
            command_executor=browserstack_url,
            desired_capabilities=browserstack_cap
        )
    else:
        geckodriver: str = f'{os.environ["pkgGeckoDriver"]}/bin/geckodriver'
        firefox: str = f'{os.environ["pkgFirefox"]}/bin/firefox'
        options = Options()
        options.add_argument('--width=1366')
        options.add_argument('--height=768')
        options.binary_location = firefox
        options.headless = True
        driver = Firefox(
            executable_path=geckodriver,
            firefox_binary=firefox,
            options=options
        )
    return driver
