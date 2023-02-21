# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
import pytest
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.support.select import (
    Select,
)
from typing import (
    Tuple,
)
import utils


def test_group_consulting(
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

    # Enter group consulting
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/consulting")
    assert utils.wait_for_text(
        driver,
        "Now we can post comments on groups",
        timeout,
    )

    # Enter group consulting not access
    driver.get(f"{asm_endpoint}/orgs/okada/groups/oneshottest/consulting")
    assert utils.wait_for_text(
        driver,
        "Access denied",
        timeout,
    )


def test_group_reports(
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
    # Enter reports
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/vulns")
    reports = utils.wait_for_id(
        driver,
        "reports",
        timeout,
    )
    reports.click()
    technical_report = utils.wait_for_id(
        driver,
        "report-excel",
        timeout,
    )
    technical_report.click()
    assert utils.wait_for_text(
        driver,
        "Verification code",
        timeout,
    )


def test_group_events(
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

    # Enter event
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/events")
    event = utils.wait_for_text(
        driver,
        "This is an eventuality with evidence",
        timeout,
    )
    event.click()
    assert utils.wait_for_text(
        driver,
        "Authorization for a special attack",
        timeout,
    )


def test_group_analytics(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    expected_charts: Tuple[str, ...] = tuple(
        (
            "Mean time to remediate (MTTR) benchmark",
            "Exposure over time",
            "Exposure by type",
            "Exposure benchmark",
            "Exposure management over time",
            "Exposure management over time (%)",
            "Exposure trends by vulnerability category",
            "Vulnerabilities treatment",
            "Vulnerabilities by source",
            "Remediation rate",
            "Total types",
            "Days until zero exposure",
            "Vulnerabilities with no treatment",
            "Vulnerabilities being re-attacked",
            "Days since last remediation",
            "Sprint exposure increment",
            "Sprint exposure decrement",
            "Sprint exposure change overall",
            "Total vulnerabilities",
            "Open vulnerabilities",
            "Severity",
            "Active resources distribution",
            "Vulnerabilities by tag",
            "Vulnerabilities by level",
            "Accepted vulnerabilities by user",
            "Vulnerabilities by assignment",
            "Status of assigned vulnerabilities",
            "Report Technique",
            "Group availability",
            "Accepted vulnerabilities by CVSS severity",
            "Exposure by assignee",
            "Files with open vulnerabilities in the last 20 weeks",
            "Mean time to remediate (MTTR) by CVSS severity",
            "Days since group is failing",
            "Mean time to request reattacks",
            "Finding by tags",
            "Your commitment towards security",
            "Builds risk",
        )
    )
    # Login
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )

    # Enter Analytics
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/analytics")

    for expected_chart in expected_charts:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )


def test_group_forces(
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

    # Enter execution summary
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/devsecops")
    utils.wait_for_text(
        driver,
        "Click on an execution to see more details",
        timeout,
    )
    assert "Identifier" in driver.page_source


def test_group_stakeholder(
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

    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/stakeholders")
    utils.wait_for_text(
        driver,
        "continuoushacking@gmail.com",
        timeout,
    )
    assert utils.wait_for_text(
        driver,
        "Stakeholder email",
        timeout,
    )

    driver.get(f"{asm_endpoint}/orgs/okada/groups/oneshottest/stakeholders")
    utils.wait_for_text(
        driver,
        "integratesuser@gmail.com",
        timeout,
    )
    assert "Registration status" in driver.page_source


@pytest.mark.skip(reason="flaky")
def test_group_scope_repositories(  # pylint: disable=too-many-locals
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

    # Add repo
    repo_url: str = "https://gitlab.com/fluidattacks/universe"
    driver.get(f"{asm_endpoint}/orgs/makimachi/groups/metropolis/scope")
    add_repo = utils.wait_for_id(
        driver,
        "git-root-add",
        timeout,
    )
    add_repo.click()
    close_tour = utils.wait_for_aria_label_by_parent(
        driver=driver,
        parent_id="react-joyride-step-0",
        parent_element="div",
        element="button",
        text="Skip",
        timeout=timeout,
    )
    close_tour.click()
    add_repo.click()
    url = utils.wait_for_name(driver, "url", timeout)
    branch = utils.wait_for_name(
        driver,
        "branch",
        timeout,
    )
    environment = utils.wait_for_name(
        driver,
        "environment",
        timeout,
    )
    credential_name = utils.wait_for_name(
        driver,
        "credentials.name",
        timeout,
    )
    credential_type = Select(
        utils.wait_for_name(
            driver,
            "credentials.typeCredential",
            timeout,
        )
    )
    url.send_keys(repo_url)
    branch.send_keys("trunk")
    environment.send_keys("production")
    credential_name.send_keys(utils.rand_name("production-credential"))
    credential_type.select_by_value("TOKEN")
    credential_token = utils.wait_for_name(
        driver,
        "credentials.token",
        timeout,
    )
    credential_token.send_keys("production-credential")
    credential_org = utils.wait_for_name(
        driver,
        "credentials.azureOrganization",
        timeout,
    )
    credential_org.send_keys("testorg1")
    reject_health_check = utils.wait_for_id(
        driver,
        "Yes",
        timeout,
    )
    reject_health_check.click()
    reject_health_a = utils.wait_for_name(
        driver,
        "healthCheckConfirm",
        timeout,
    )
    reject_health_a.click()
    proceed = utils.wait_for_id(
        driver,
        "git-root-add-confirm",
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        repo_url,
        timeout,
    )


def test_group_scope_environments(
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

    # Show all columns
    driver.execute_script('localStorage.setItem("rootTableSet", "{}")')
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/scope")

    # Add environment
    table_row = utils.wait_for_text(
        driver,
        "https://gitlab.com/fluidattacks/universe",
        timeout,
    )
    table_row.click()
    envs_tab = utils.wait_for_id(
        driver,
        "envsTab",
        timeout,
    )
    envs_tab.click()

    utils.wait_for_id(
        driver,
        "add-env-url",
        timeout,
    ).click()

    add_environment_url_button = utils.wait_for_id(
        driver,
        "add-env-url-confirm",
        timeout,
    )

    url_input = utils.wait_for_name(
        driver,
        "url",
        timeout,
    )
    assert add_environment_url_button.get_attribute("disabled")

    url_input.send_keys("https://login.microsoftonline.com/")
    url_type_input = Select(
        utils.wait_for_name(
            driver,
            "urlType",
            timeout,
        )
    )
    url_type_input.select_by_index("3")
    assert add_environment_url_button.get_attribute("disabled") is None

    add_environment_url_button.click()


def test_group_scope_files(
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

    # Enter Scope
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/scope")
    assert utils.wait_for_text(
        driver,
        "test.zip",
        timeout,
    )


def test_group_scope_portfolio(
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

    # Add tag
    tag_name: str = utils.rand_name("test-portfolio")
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/scope")
    add_tag = utils.wait_for_id(
        driver,
        "portfolio-add",
        timeout,
    )
    add_tag.click()
    tags = utils.wait_for_name(driver, "tags[0]", timeout)
    tags.send_keys(tag_name)
    proceed = utils.wait_for_id(
        driver,
        "portfolio-add-confirm",
        timeout,
    )

    proceed.click()
    assert utils.wait_for_text(
        driver,
        tag_name,
        timeout,
    )
