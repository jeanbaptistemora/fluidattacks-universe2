from base64 import (
    b64encode,
)
from itsdangerous import (
    TimestampSigner,
)
import json
from model import (
    Credentials,
)
from random import (
    randint,
)
from selenium.webdriver.common.by import (
    By,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.remote.webelement import (
    WebElement,
)
from selenium.webdriver.support import (
    expected_conditions as ec,
)
from selenium.webdriver.support.ui import (
    WebDriverWait,
)
from uuid import (
    uuid4 as uuid,
)


def wait_for_id(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located(
            (
                By.ID,
                text,
            )
        )
    )


def wait_for_text(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                f"//*[text()[contains(., '{text}')]]",
            )
        )
    )


def wait_for_class_name(
    driver: WebDriver, text: str, timeout: int
) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((By.CLASS_NAME, text))
    )


def wait_for_hide_text(
    driver: WebDriver, text: str, timeout: int
) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until_not(
        ec.presence_of_element_located(
            (
                By.XPATH,
                f"//*[text()[contains(., '{text}')]]",
            )
        )
    )


def wait_for_hide_class_name(
    driver: WebDriver, text: str, timeout: int
) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until_not(
        ec.presence_of_element_located((By.CLASS_NAME, text))
    )


def wait_for_url(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(ec.url_contains(text))


def wait_for_name(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located(
            (
                By.NAME,
                text,
            )
        )
    )


def move_to_element(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script(
        'arguments[0].scrollIntoView({block: "center"});',
        element,
    )


def rand_name(prefix: str) -> str:
    return f"{prefix}-{randint(0, 1000)}"


def login(
    driver: WebDriver, asm_endpoint: str, credentials: Credentials
) -> None:
    driver.get(asm_endpoint)
    signer = TimestampSigner(credentials.key)

    session_cookie = signer.sign(
        b64encode(
            json.dumps(
                {
                    "username": credentials.user,
                    "first_name": "",
                    "last_name": "",
                    "session_key": uuid().hex,
                }
            ).encode()
        )
    ).decode()

    driver.add_cookie(
        {
            "name": "session",
            "value": session_cookie,
        }
    )
