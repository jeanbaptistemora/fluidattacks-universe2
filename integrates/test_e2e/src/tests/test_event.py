# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_event(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter event
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/events')
    event = utils.wait_for_text(
        driver,
        'This is an eventuality with evidence',
        timeout,
    )
    event.click()
    utils.wait_for_text(
        driver,
        'unittest@fluidattacks.com',
        timeout,
    )
    assert 'unittest@fluidattacks.com' in driver.page_source
