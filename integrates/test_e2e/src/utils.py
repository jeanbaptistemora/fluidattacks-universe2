# Standard libraries
from random import randint

# Third party libraries
from pyotp import TOTP
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# Local libraries
from model import (
    AzureCredentials
)


def otp_azure(azure_credentials: AzureCredentials) -> str:
    totp: TOTP = TOTP(azure_credentials.seed)
    return str(totp.now())


def wait_for_id(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located((
            By.ID,
            text,
        ))
    )


def wait_for_text(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((
            By.XPATH,
            f"//*[text()[contains(., '{text}')]]",
        ))
    )


def wait_for_url(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.url_contains(text)
    )


def wait_for_name(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((
            By.NAME,
            text,
        ))
    )


def move_to_element(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script(
        'arguments[0].scrollIntoView({block: "center"});',
        element,
    )


def rand_name(prefix: str) -> str:
    return f'{prefix}-{randint(0, 1000)}'


def login_azure(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        timeout: int) -> None:
    # Load login page
    driver.get('https://login.microsoftonline.com/')

    # Input user and click next
    input_user = wait_for_id(
        driver,
        'i0116',
        timeout,
    )
    input_user.send_keys(azure_credentials.user)
    btn_next = wait_for_id(
        driver,
        'idSIButton9',
        timeout,
    )
    btn_next.click()

    # Input password and click login
    input_password = wait_for_id(
        driver,
        'i0118',
        timeout,
    )
    input_password.send_keys(azure_credentials.password)
    btn_login = wait_for_id(
        driver,
        'idSIButton9',
        timeout,
    )
    btn_login.click()

    # Input otp and click verify
    input_otp = wait_for_id(
        driver,
        'idTxtBx_SAOTCC_OTC',
        timeout,
    )
    input_otp.send_keys(otp_azure(azure_credentials))
    btn_verify = wait_for_id(
        driver,
        'idSubmit_SAOTCC_Continue',
        timeout,
    )
    btn_verify.click()

    # Wait for home
    wait_for_url(driver, 'office.com', timeout)


def login_integrates_azure(
        driver: WebDriver,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Load login page
    driver.get(integrates_endpoint)

    # Login with microsoft
    btn_login = wait_for_id(
        driver,
        'login-microsoft',
        timeout,
    )
    btn_login.click()

    # Wait for home
    wait_for_url(driver, f'{integrates_endpoint}/orgs/', timeout)
