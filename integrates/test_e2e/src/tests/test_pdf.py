# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_pdf(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Get reports
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    reports = utils.wait_for_id(
        driver,
        'reports',
        timeout,
    )
    reports.click()

    # Get reports popup
    utils.wait_for_text(
        driver,
        'Reports are created on-demand',
        timeout,
    )
    assert 'Reports are created on-demand' in driver.page_source
