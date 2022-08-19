# pylint: disable=import-error, useless-suppression
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.support.ui import (
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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
        "unittest@fluidattacks.com",
        timeout,
    )


def test_group_analytics(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    expected_charts: Tuple[str, ...] = tuple(
        (
            "MTTR Benchmarking",
            "Total Exposure",
            "Open Exposure by type",
            "Exposure over time",
            "Distribution over time",
            "Exposure Trends by Categories",
            "Vulnerabilities treatment",
            "Vulnerabilities by source",
            "Total types",
            "Days until zero exposure",
            "Treatmentless vulnerabilities",
            "Vulnerabilities being re-attacked",
            "Days since last remediation",
            "Total vulnerabilities",
            "Sprint exposure increment",
            "Sprint exposure decrement",
            "Sprint exposure change overall",
            "Mean time to reattack",
            "Severity",
            "Active resources distribution",
            "Vulnerabilities by tag",
            "Vulnerabilities by level",
            "Accepted vulnerabilities by user",
            "Vulnerabilities by assignment",
            "Status of assigned vulnerabilities",
            "Report Technique",
            "Group availability",
            "Accepted vulnerabilities by severity",
            "Exposure by assignment",
            "Files with open vulnerabilities in the last 20 weeks",
            "Mean (average) days to remediate",
            "Days since group is failing",
            "Finding by tags",
            "Your commitment towards security",
            "Builds risk",
        )
    )
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter execution summary
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/devsecops")
    utils.wait_for_text(
        driver,
        "Click on an execution to see more details",
        timeout,
    )
    assert "Identifier" in driver.page_source


def test_group_scope_repositories(  # pylint: disable=too-many-locals
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Add repo
    repo_url: str = "https://gitlab.com/fluidattacks/universe"
    driver.get(f"{asm_endpoint}/orgs/makimachi/groups/metropolis/scope")
    add_repo = utils.wait_for_id(
        driver,
        "git-root-add",
        timeout,
    )
    add_repo.click()
    close_tour = utils.wait_for_aria_label(
        driver,
        "button",
        "Skip",
        timeout,
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
            "credentials.type",
            timeout,
        )
    )
    url.send_keys(repo_url)
    branch.send_keys("trunk")
    environment.send_keys("production")
    credential_name.send_keys(utils.rand_name("production-credential"))
    credential_type.select_by_value("HTTPS")
    credential_token = utils.wait_for_name(
        driver,
        "credentials.token",
        timeout,
    )
    credential_token.send_keys("production-credential")
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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

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
