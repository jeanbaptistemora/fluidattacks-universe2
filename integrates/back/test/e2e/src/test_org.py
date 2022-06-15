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
    "Exposure remediation rate (benchmark)",
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
    "Treatmentless vulnerabilities",
    "Vulnerabilities being re-attacked",
    "Days since last remediation",
    "Total vulnerabilities",
    "Severity increased in Sprint",
    "Severity remediated in Sprint",
    "Sprint remediation Overall",
    "Severity",
    "Active resources distribution",
    "Vulnerabilities by tag",
    "Vulnerabilities by level",
    "Accepted vulnerabilities by user",
    "Unsolved events by groups",
    "How many vulnerabilities are remediated (closed)?",
    "How many vulnerabilities are remediated and accepted?",
    "Types of Vulnerabilities by Group",
    "Open Types of Vulnerabilities by Group",
    "Top Oldest Types of Vulnerabilities",
    "Undefined Treatment by Group",
    "Vulnerabilities by group",
    "Open vulnerabilities by group",
    "Vulnerabilities by assignment",
    "Status of assigned vulnerabilities",
    "Accepted vulnerabilities by severity",
    "Severity by assignment",
    "Files with open vulnerabilities in the last 20 weeks",
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

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3_30&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3_90&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
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
    group_name = "akame"
    group_description: str = "test-group-description"
    driver.get(f"{asm_endpoint}/orgs/okada/groups")
    add_group = utils.wait_for_id(
        driver,
        "add-group",
        timeout,
    )
    add_group.click()
    close_tour = utils.wait_for_aria_label(
        driver,
        "button",
        "Skip",
        timeout,
    )
    close_tour.click()
    add_group.click()
    name = utils.wait_for_id(driver, "add-group-name", timeout)
    name.send_keys(group_name)
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
