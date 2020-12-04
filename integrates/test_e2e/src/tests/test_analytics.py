# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_analytics(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Get Analytics
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/')
    utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )
    assert 'Vulnerabilities over time' in driver.page_source
