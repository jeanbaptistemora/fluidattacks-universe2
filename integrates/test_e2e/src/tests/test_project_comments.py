# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_project_comments(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter project comments
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/consulting')
    utils.wait_for_text(
        driver,
        'Now we can post comments on projects',
        timeout,
    )
    assert 'Now we can post comments on projects' in driver.page_source
