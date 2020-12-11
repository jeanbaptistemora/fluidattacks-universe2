# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    Credentials
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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter dashboard
    driver.get(f'{integrates_endpoint}/orgs/')
    assert utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )
