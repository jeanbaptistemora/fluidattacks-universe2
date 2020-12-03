# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver


def test_login_screen(driver: WebDriver, integrates_endpoint: str,) -> None:
    driver.get(integrates_endpoint)
    assert 'FluidIntegrates' in driver.page_source
    driver.quit()
