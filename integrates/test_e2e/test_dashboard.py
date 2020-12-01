# Standard libraries
from typing import Any, Dict

# Third party libraries
from selenium import webdriver

# Local libraries
import helpers


def test_dashboard(
        browserstack_cap: Dict[str, str],
        bitbucket_credentials: Dict[str, str],
        browserstack_url: str) -> None:
    browserstack_cap['name'] = test_dashboard.__name__

    driver: Any = webdriver.Remote(
        command_executor=browserstack_url,
        desired_capabilities=browserstack_cap
    )

    helpers.login_bitbucket(driver, bitbucket_credentials)

    driver.quit()
