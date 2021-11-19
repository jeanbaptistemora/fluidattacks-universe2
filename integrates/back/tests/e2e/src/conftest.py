from model import (
    Credentials,
)
import os
import pytest
from selenium.webdriver import (
    Firefox,
)
from selenium.webdriver.firefox.options import (
    Options,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from typing import (
    Iterable,
)


@pytest.fixture(autouse=True, scope="session")
def path_geckodriver() -> str:
    return f'{os.environ["pkgGeckoDriver"]}/bin/geckodriver'


@pytest.fixture(autouse=True, scope="session")
def path_firefox() -> str:
    return f'{os.environ["pkgFirefox"]}/bin/firefox'


@pytest.fixture(autouse=True, scope="session")
def branch() -> str:
    return os.environ["CI_COMMIT_REF_NAME"]


@pytest.fixture(autouse=True, scope="session")
def is_ci() -> bool:
    return bool(os.environ.get("CI", False))


@pytest.fixture(autouse=True, scope="session")
def timeout() -> int:
    return 20


@pytest.fixture(autouse=True, scope="session")
def credentials() -> Credentials:
    node_index: int = (
        int(os.environ["CI_NODE_INDEX"])
        if "CI_NODE_INDEX" in os.environ
        else 1
    )
    user: str = os.environ[f"TEST_E2E_USER_{node_index}"]
    key: str = os.environ["STARLETTE_SESSION_KEY"]
    return Credentials(
        user=user,
        key=key,
    )


@pytest.fixture(autouse=True, scope="session")
def asm_endpoint(
    branch: str,  # pylint: disable=redefined-outer-name
    is_ci: bool,  # pylint: disable=redefined-outer-name
) -> str:
    if branch == "master":
        raise NotImplementedError("e2e is only designed to run in dev env")

    return (
        f"https://{branch}.app.fluidattacks.com"
        if is_ci
        else "https://localhost:8001"
    )


@pytest.fixture(autouse=True, scope="function")
def driver(
    path_geckodriver: str,  # pylint: disable=redefined-outer-name
    path_firefox: str,  # pylint: disable=redefined-outer-name
    is_ci: bool,  # pylint: disable=redefined-outer-name
) -> Iterable[WebDriver]:
    options = Options()
    options.binary_location = path_firefox
    options.headless = is_ci
    web_driver: WebDriver = Firefox(
        executable_path=path_geckodriver,
        firefox_binary=path_firefox,
        options=options,
    )
    try:
        web_driver.maximize_window()
        yield web_driver
    finally:
        web_driver.quit()
