# Third party libraries
from selenium.webdriver import Remote


def test_login_screen(driver: Remote, endpoint: str,) -> None:
    driver.get(endpoint)
    assert 'FluidIntegrates' in driver.page_source
    driver.quit()
