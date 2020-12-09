# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_others_login_screen(
        driver: WebDriver,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Enter login screen
    driver.get(integrates_endpoint)
    assert utils.wait_for_text(
        driver,
        'Please authenticate to proceed.',
        timeout,
    )


def test_others_dashboard(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter dashboard
    assert utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )
