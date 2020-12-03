# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_dashboard(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str) -> None:
    utils.login_azure(driver, azure_credentials)
    utils.login_integrates_azure(driver, integrates_endpoint)
    driver.quit()
