# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_tracking(
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

    # Enter finding tracking
    severity = utils.wait_for_id(
        driver,
        'trackingItem',
        timeout,
    )
    severity.click()
    utils.wait_for_text(
        driver,
        '2020-09-09',
        timeout,
    )
    assert '2020-09-09' in driver.page_source
