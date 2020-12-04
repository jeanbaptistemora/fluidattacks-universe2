# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_finding(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding description
    description = utils.wait_for_text(
        driver,
        'Description',
        timeout,
    )
    description.click()
    utils.wait_for_text(
        driver,
        'R359. Avoid using generic exceptions.',
        timeout,
    )
    assert 'The source code uses generic ' \
        'exceptions to handle unexpected errors' in driver.page_source
