from _pytest.fixtures import (
    FixtureRequest,
)
from appium import (
    webdriver,
)
from appium.webdriver.webdriver import (
    WebDriver,
)
import os
import pytest
import time


def open_ephemeral(appium_driver: WebDriver) -> None:
    host_url: str = "exp://exp.host/@developmentatfluid/fluidattacks"
    branch_name: str = os.environ["CI_COMMIT_REF_NAME"]
    load_delay: int = 10
    # https://docs.expo.io/workflow/debugging/#developer-menu
    devmenu_close_keycode: int = 82

    time.sleep(load_delay)
    appium_driver.execute_script(
        "mobile:deepLink",
        {
            "package": "host.exp.exponent",
            "url": f"{host_url}?release-channel={branch_name}",
        },
    )
    time.sleep(load_delay)
    appium_driver.keyevent(devmenu_close_keycode)


@pytest.fixture  # type: ignore
def driver(request: FixtureRequest) -> WebDriver:
    # Setup
    appium_driver: WebDriver = webdriver.Remote("http://localhost:4723/wd/hub")
    open_ephemeral(appium_driver)

    # Teardown
    request.addfinalizer(appium_driver.quit)

    return appium_driver
