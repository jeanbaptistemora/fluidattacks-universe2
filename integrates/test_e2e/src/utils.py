# Third party libraries
from pyotp import TOTP
from selenium.webdriver.remote.webdriver import WebDriver
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


def login_azure(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        timeout: int) -> None:
    # Load login page
    driver.get('https://login.microsoftonline.com/')

    # Input user and click next
    input_user = driver.find_element_by_id('i0116')
    input_user.send_keys(azure_credentials.user)
    btn_next = driver.find_element_by_id('idSIButton9')
    btn_next.click()

    # Input password and click login
    wait_for_id(driver, 'i0118', timeout)
    input_password = driver.find_element_by_id('i0118')
    input_password.send_keys(azure_credentials.password)

    btn_login = driver.find_element_by_id('idSIButton9')
    btn_login.click()

    # Input otp and click verify
    wait_for_id(driver, 'idTxtBx_SAOTCC_OTC', timeout)
    input_otp = driver.find_element_by_id('idTxtBx_SAOTCC_OTC')
    input_otp.send_keys(otp_azure(azure_credentials))
    btn_verify = driver.find_element_by_id('idSubmit_SAOTCC_Continue')
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
    btn_login = driver.find_element_by_id('login-microsoft')
    btn_login.click()

    # Wait for home
    wait_for_url(driver, f'{integrates_endpoint}/orgs/', timeout)
