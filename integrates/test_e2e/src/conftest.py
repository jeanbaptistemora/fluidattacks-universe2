# Standard libraries
import os
from typing import Iterable

# Third party libraries
import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

# Local libraries
from model import (
    Credentials,
)


@pytest.fixture(autouse=True, scope='session')
def path_geckodriver() -> str:
    return f'{os.environ["pkgGeckoDriver"]}/bin/geckodriver'


@pytest.fixture(autouse=True, scope='session')
def path_firefox() -> str:
    return f'{os.environ["pkgFirefox"]}/bin/firefox'


@pytest.fixture(autouse=True, scope='session')
def branch() -> str:
    return os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')
def is_ci() -> bool:
    return bool(os.environ['CI'])


@pytest.fixture(autouse=True, scope='session')
def timeout() -> int:
    return 30


@pytest.fixture(autouse=True, scope='session')
def credentials() -> Credentials:
    user: str = os.environ['TEST_E2E_USER']
    key: str = os.environ['STARLETTE_SESSION_KEY']
    return Credentials(
        user=user,
        key=key,
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
        path_geckodriver: str,
        path_firefox: str,
        is_ci: bool) -> Iterable[WebDriver]:
    options = Options()
    options.binary_location = path_firefox
    options.headless = is_ci
    driver: WebDriver = Firefox(
        executable_path=path_geckodriver,
        firefox_binary=path_firefox,
        options=options
    )
    try:
        driver.maximize_window()
        yield driver
    finally:
        driver.quit()
