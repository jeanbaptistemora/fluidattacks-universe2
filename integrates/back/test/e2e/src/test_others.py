# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
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
    assert utils.wait_for_id(
        driver,
        "login-auth",
        timeout,
    )


def test_others_dashboard(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    # Login
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )

    # Enter dashboard
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")
    assert utils.wait_for_text(
        driver,
        "Exposure management over time",
        timeout,
    )
