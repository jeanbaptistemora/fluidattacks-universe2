# Standard libraries
from typing import Dict

# Third party libraries
from selenium.webdriver import Remote

# Local libraries
import utils


def test_dashboard(
        driver: Remote,
        bitbucket_credentials: Dict[str, str]) -> None:
    utils.login_bitbucket(driver, bitbucket_credentials)
    driver.quit()
