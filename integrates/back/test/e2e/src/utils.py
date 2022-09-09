# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error, useless-suppression
from datetime import (
    datetime,
    timedelta,
)
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
from selenium.webdriver.support import (
    expected_conditions as ec,
)
from selenium.webdriver.support.ui import (
    WebDriverWait,
)
from session_token import (
    calculate_hash_token,
    new_encoded_jwt,
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


def wait_for_aria_label(
    driver: WebDriver, element: str, text: str, timeout: int
) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located(
            (
                By.XPATH,
                f"//{element}[@aria-label='{text}']",
            )
        )
    )


def wait_for_aria_label_by_parent(
    *,
    driver: WebDriver,
    parent_id: str,
    parent_element: str,
    element: str,
    text: str,
    timeout: int,
) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located(
            (
                By.XPATH,
                f"//{parent_element}[@id='{parent_id}']"
                + f"//{element}[@aria-label='{text}']",
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


def wait_for_name(driver: WebDriver, text: str, timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located(
            (
                By.NAME,
                text,
            )
        )
    )


def rand_name(prefix: str) -> str:
    return f"{prefix}-{randint(0, 1000)}"


def login(
    driver: WebDriver,
    asm_endpoint: str,
    credentials: Credentials,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    driver.get(asm_endpoint)
    jti = calculate_hash_token()["jti"]
    jwt_token: str = new_encoded_jwt(
        dict(
            user_email=credentials.user,
            first_name="",
            last_name="",
            exp=datetime.utcnow() + timedelta(seconds=86400),
            sub="test_e2e_session",
            jti=jti,
        ),
        jwt_encryption_key,
        jwt_secret,
    )

    driver.add_cookie(
        {
            "name": "integrates_session",
            "value": jwt_token,
        }
    )
