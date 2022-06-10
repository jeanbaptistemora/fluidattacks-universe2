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
    technical_report = utils.wait_for_text(
        driver,
        "Technical",
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
            "Open Severity by type",
            "Severity over time",
            "Distribution over time",
            "Vulnerabilities treatment",
            "Vulnerabilities by source",
            "Total types",
            "Days until zero exposure",
            "Vulnerabilities with not-defined treatment",
            "Vulnerabilities being re-attacked",
            "Days since last remediation",
            "Total vulnerabilities",
            "Severity increased in Sprint",
            "Severity remediated in Sprint",
            "Sprint remediation Overall",
            "Severity",
            "Active resources distribution",
            "Systems Risk",
            "Vulnerabilities by tag",
            "Vulnerabilities by level",
            "Accepted vulnerabilities by user",
            "Vulnerabilities by assignment",
            "Accepted vulnerabilities by severity",
            "Severity by assignment",
            "Files with open vulnerabilities in the last 20 weeks",
            "Mean (average) days to remediate",
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


def test_group_scope_repositories(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Add repo
    repo_url: str = utils.rand_name("https://gitlab.com/fluidattacks/test")
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/scope")
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
    url.send_keys(repo_url)
    branch.send_keys("master")
    environment.send_keys("production")
    reject_health_check = utils.wait_for_id(
        driver,
        "No",
        timeout,
    )
    reject_health_check.click()
    reject_health_a = utils.wait_for_name(
        driver,
        "healthCheckConfirm",
        timeout,
    )
    reject_health_a.click()
    checkboxes = driver.find_elements_by_css_selector("input[type='checkbox']")
    for checkbox in checkboxes[1:]:
        if not checkbox.is_selected():
            checkbox.click()
    proceed = utils.wait_for_id(
        driver,
        "git-root-add-proceed",
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
        "https://gitlab.com/fluidattacks/product",
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
        "add-environment-url-button",
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
        "portfolio-add-proceed",
        timeout,
    )

    proceed.click()
    assert utils.wait_for_text(
        driver,
        tag_name,
        timeout,
    )
