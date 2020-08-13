# 3rd party
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement


def test_01_init_page(driver: WebDriver) -> None:
    google_button: WebElement = driver.find_element_by_accessibility_id(
        'Sign in with Google')
    assert google_button.is_displayed()
