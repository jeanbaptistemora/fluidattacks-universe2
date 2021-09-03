from model import (  # pylint: disable=import-error
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
import utils


def test_others_login_screen(
    driver: WebDriver, asm_endpoint: str, timeout: int
) -> None:
    # Enter login screen
    driver.get(asm_endpoint)
    assert utils.wait_for_text(
        driver,
        "please authenticate to proceed.",
        timeout,
    )


def test_others_dashboard(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter dashboard
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")
    assert utils.wait_for_text(
        driver,
        "Severity over time",
        timeout,
    )
