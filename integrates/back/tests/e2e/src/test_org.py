# pylint: disable=import-error, useless-suppression
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from typing import (
    List,
)
import utils

EXPECTED_MANY_GROUPS_CHARTS: List[str] = [
    "Remediation Rate Benchmarking",
    "MTTR Benchmarking",
    "Total Exposure",
    "Open Severity by type",
    "Open Severity by groups",
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
    "Severity",
    "Active resources distribution",
    "Vulnerabilities by tag",
    "Vulnerabilities by level",
    "Accepted vulnerabilities by user",
    "Unsolved events by groups",
    "How many vulnerabilities are remediated (closed)?",
    "How many vulnerabilities are remediated and accepted?",
    "Findings by group",
    "Open findings by group",
    "Top oldest findings",
    "Treatmentless by group",
    "Vulnerabilities by treatments",
    "Vulnerabilities by group",
    "Open vulnerabilities by group",
    "Accepted vulnerabilities by severity",
    "Mean (average) days to remediate",
    "Tags by groups",
]


def test_org_analytics(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter Analytics
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")

    for expected_chart in EXPECTED_MANY_GROUPS_CHARTS:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )


def test_org_groups(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Add group
    group_description: str = "test-group-description"
    driver.get(f"{asm_endpoint}/orgs/okada/groups")
    add_group = utils.wait_for_id(
        driver,
        "add-group",
        timeout,
    )
    add_group.click()
    description = utils.wait_for_id(driver, "add-group-description", timeout)
    description.send_keys(group_description)
    proceed = utils.wait_for_id(
        driver,
        "add-group-proceed",
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        "Group created successfully",
        timeout,
    )


def test_org_portfolios(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter portfolio
    driver.get(f"{asm_endpoint}/orgs/okada/portfolios")
    test_groups = utils.wait_for_text(
        driver,
        "test-groups",
        timeout,
    )
    test_groups.click()
    for expected_chart in EXPECTED_MANY_GROUPS_CHARTS:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )
