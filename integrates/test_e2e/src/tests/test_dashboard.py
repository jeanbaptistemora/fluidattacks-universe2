# Standard libraries
from typing import Dict

# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils


def test_dashboard(
        driver: WebDriver,
        azure_credentials: Dict[str, str],
        endpoint: str) -> None:
    utils.login_azure(driver, azure_credentials)
    utils.login_integrates_azure(driver, endpoint)
    driver.quit()
