# Standard libraries
import os
from typing import Iterable

# Third party libraries
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver import Firefox, Remote
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

# Local libraries
from model import (
    AzureCredentials,
    BrowserStackCapacity,
)


@pytest.fixture(autouse=True, scope='session')
def browserstack_url() -> str:
    user: str = os.environ['BROWSERSTACK_USER']
    key: str = os.environ['BROWSERSTACK_KEY']
    return f'https://{user}:{key}@hub-cloud.browserstack.com/wd/hub'


@pytest.fixture(autouse=True, scope='function')
def browserstack_cap(
        branch: str,
        request: FixtureRequest) -> BrowserStackCapacity:
    return BrowserStackCapacity(
        os='Windows',
        os_version='10',
        browser='Chrome',
        browser_version='80',
        name=f'{branch}::{request.node.name}',
    )


@pytest.fixture(autouse=True, scope='session')
def branch() -> str:
    return os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')
def is_ci() -> bool:
    return bool(os.environ['CI'])


@pytest.fixture(autouse=True, scope='session')
def timeout() -> int:
    return 20


@pytest.fixture(autouse=True, scope='session')
def azure_credentials() -> AzureCredentials:
    user: str = os.environ['TEST_E2E_AZURE_USER']
    password: str = os.environ['TEST_E2E_AZURE_PASS']
    seed: str = os.environ['TEST_E2E_AZURE_SEED']
    return AzureCredentials(
        user=user,
        password=password,
        seed=seed,
    )


@pytest.fixture(autouse=True, scope='session')
def integrates_endpoint(branch: str, is_ci: bool) -> str:
    url: str = ''
    if branch == 'master':
        url = 'https://integrates.fluidattacks.com'
    elif is_ci:
        url = f'https://{branch}.integrates.fluidattacks.com'
    else:
        url = 'https://localhost:8081'
    return url


@pytest.fixture(autouse=True, scope='function')
def driver(
        browserstack_cap: BrowserStackCapacity,
        browserstack_url: str,
        is_ci: bool) -> Iterable[WebDriver]:
    driver: WebDriver = None
    if is_ci:
        driver = Remote(
            command_executor=browserstack_url,
            desired_capabilities=browserstack_cap._asdict()
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
    try:
        yield driver
    finally:
        driver.quit()
