# Standard libraries
from typing import Dict

# Third party libraries
from selenium.webdriver import Remote

# Local libraries
import utils


def test_dashboard(
        driver: Remote,
        azure_credentials: Dict[str, str],
        endpoint: str) -> None:
    utils.login_azure(driver, azure_credentials)
    utils.login_integrates_azure(driver, endpoint)
    driver.quit()
