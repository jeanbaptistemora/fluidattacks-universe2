from model import (  # pylint: disable=import-error
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from typing import (
    List,
)
import utils


def test_org_analytics(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
) -> None:
    expected_charts: List[str] = [
        "Remediation Rate Benchmarking",
        "MTTR Benchmarking",
        "Severity over time",
        "Distribution over time",
        "Vulnerabilities treatment",
        "Total types",
        "Severity",
        "Days since last remediation",
        "Total vulnerabilities",
    ]

    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter Analytics
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")

    for expected_chart in expected_charts:
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
    expected_charts: List[str] = [
        "Severity over time",
        "How many vulnerabilities are remediated (closed)?",
        "How many vulnerabilities are remediated and accepted?",
        "Findings by group",
        "Open findings by group",
        "Vulnerabilities status",
        "Vulnerabilities treatment",
        "Vulnerabilities by group",
        "Open vulnerabilities by group",
        "Treatmentless by group",
        "Severity",
        "Days since last remediation",
        "Total vulnerabilities",
    ]
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter portfolio
    driver.get(f"{asm_endpoint}/orgs/okada/portfolios")
    test_groups = utils.wait_for_text(
        driver,
        "test-projects",
        timeout,
    )
    test_groups.click()
    for expected_chart in expected_charts:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )
