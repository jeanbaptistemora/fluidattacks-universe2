# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils


def test_login_screen(
        driver: WebDriver,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Get login screen
    driver.get(integrates_endpoint)
    utils.wait_for_text(
        driver,
        'Please authenticate to proceed.',
        timeout,
    )
    assert 'FluidIntegrates' in driver.page_source
