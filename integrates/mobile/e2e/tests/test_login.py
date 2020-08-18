# 3rd party
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement


def test_01_init_page(driver: WebDriver) -> None:
    bitbucket_button: WebElement = driver.find_element_by_xpath(
        '//*[@text="Sign in with Bitbucket"]')
    assert bitbucket_button.is_displayed()
    google_button: WebElement = driver.find_element_by_xpath(
        '//*[@text="Sign in with Google"]')
    assert google_button.is_displayed()
    microsoft_button: WebElement = driver.find_element_by_xpath(
        '//*[@text="Sign in with Microsoft"]')
    assert microsoft_button.is_displayed()
