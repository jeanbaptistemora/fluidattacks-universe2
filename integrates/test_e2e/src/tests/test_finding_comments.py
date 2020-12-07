# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_finding_comments(
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

    # Enter finding comments
    comments = utils.wait_for_id(
        driver,
        'commentItem',
        timeout,
    )
    comments.click()
    utils.wait_for_text(
        driver,
        'This is a comenting test',
        timeout,
    )
    assert 'This is a comenting test' in driver.page_source
