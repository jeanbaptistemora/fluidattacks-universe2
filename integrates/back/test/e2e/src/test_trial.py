# pylint: disable=import-error, too-many-locals, useless-suppression
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.support.select import (
    Select,
)
from time import (
    sleep,
)
import utils


def test_trial_onboarding(
    driver: WebDriver,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    credentials = Credentials(user="jdoe@testcompany.com")
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )
    driver.get(f"{asm_endpoint}/home")

    assert utils.wait_for_text(driver, "Looks like", timeout)
    start_button = utils.wait_for_text(driver, "Start free trial", timeout)
    start_button.click()

    assert utils.wait_for_text(driver, "Add a code repository", timeout)
    repo_url = utils.wait_for_aria_label(driver, "input", "url", timeout)
    repo_url.send_keys("https://gitlab.com/fluidattacks/demo")
    branch = utils.wait_for_aria_label(driver, "input", "branch", timeout)
    branch.send_keys("main")
    credentials_type = Select(
        utils.wait_for_aria_label(
            driver, "select", "credentials.typeCredential", timeout
        )
    )
    credentials_type.select_by_value("USER")
    credentials_name = utils.wait_for_aria_label(
        driver, "input", "credentials.name", timeout
    )
    credentials_name.send_keys("demo")
    credentials_user = utils.wait_for_aria_label(
        driver, "input", "credentials.user", timeout
    )
    credentials_user.send_keys("demo")
    credentials_password = utils.wait_for_aria_label(
        driver, "input", "credentials.password", timeout
    )
    credentials_password.send_keys("demo")
    environment = utils.wait_for_aria_label(driver, "input", "env", timeout)
    environment.send_keys("production")
    next_button = utils.wait_for_text(driver, "Next", timeout)
    next_button.click()

    assert utils.wait_for_text(driver, "Name your organization", timeout)
    organization_name = utils.wait_for_aria_label(
        driver, "input", "organizationName", timeout
    )
    organization_name.send_keys("testco")
    organization_country = Select(
        utils.wait_for_aria_label(
            driver, "select", "organizationCountry", timeout
        )
    )
    sleep(5)
    organization_country.select_by_value("Colombia")
    group_name = utils.wait_for_aria_label(
        driver, "input", "groupName", timeout
    )
    group_name.send_keys("demo")
    report_language = Select(
        utils.wait_for_aria_label(driver, "select", "reportLanguage", timeout)
    )
    report_language.select_by_value("EN")
    group_description = utils.wait_for_aria_label(
        driver, "textarea", "groupDescription", timeout
    )
    group_description.send_keys("demo")
    start_trial_button = utils.wait_for_text(
        driver, "Start Free Trial", timeout
    )
    start_trial_button.click()

    assert utils.wait_for_text(driver, "Our Machine is running", timeout)
    close_button = utils.wait_for_id(driver, "close-standby", timeout)
    close_button.click()

    assert utils.wait_for_text(driver, "Git Roots", timeout)
    assert utils.wait_for_text(
        driver, "https://gitlab.com/fluidattacks/demo", timeout
    )
    assert utils.wait_for_text(driver, "Queued", timeout)
