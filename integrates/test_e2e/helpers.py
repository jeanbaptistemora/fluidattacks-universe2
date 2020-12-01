# Standard libraries
from typing import Any, Dict

# Third party libraries
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def login_bitbucket(
        driver: Any,
        bitbucket_credentials: Dict[str, str]) -> None:
    driver.get('https://id.atlassian.com/login')

    input_user = driver.find_element_by_id('username')
    input_user.send_keys(bitbucket_credentials['user'])

    btn_login = driver.find_element_by_id('login-submit')
    btn_login.click()

    input_password = driver.find_element_by_id('password')
    input_password.send_keys(bitbucket_credentials['password'])

    btn_login.click()

    WebDriverWait(driver, 10).until(
        ec.url_matches('https://start.atlassian.com/')
    )
