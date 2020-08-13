# Standard Imports
from time import sleep

# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from appium import webdriver
from appium.webdriver.webdriver import WebDriver


def open_ephemeral(appium_driver: WebDriver) -> None:
    host_url: str = 'exp://exp.host/@developmentatfluid/integrates'
    branch_name: str = 'someoneatfluid'
    appium_driver.get(f'{host_url}?release-channel={branch_name}')
    experience_load_delay_ms: int = 2000
    sleep(experience_load_delay_ms)


@pytest.fixture  # type: ignore
def driver(request: FixtureRequest) -> WebDriver:
    # Setup
    appium_driver: WebDriver = webdriver.Remote('http://localhost:4723/wd/hub')
    open_ephemeral(appium_driver)

    # Teardown
    request.addfinalizer(appium_driver.quit)

    return appium_driver
