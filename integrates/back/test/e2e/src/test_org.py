# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
from selenium.common.exceptions import (
    TimeoutException,
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
    "Open Exposure by type",
    "Open Exposure by groups",
    "Aggregated exposure benchmark",
    "Exposure over time",
    "Distribution over time",
    "Exposure Trends by Categories",
    "Vulnerabilities treatment",
    "Vulnerabilities by source",
    "Remediation Rate",
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
    "Mean time to reattack",
    "Severity",
    "Active resources distribution",
    "Vulnerabilities by tag",
    "Vulnerabilities by level",
    "Accepted vulnerabilities by user",
    "Unsolved events by groups",
    "How many vulnerabilities are remediated and accepted?",
    "Types of Vulnerabilities by Group",
    "Open Types of Vulnerabilities by Group",
    "Top Oldest Types of Vulnerabilities",
    "Vulnerabilities by group",
    "Open vulnerabilities by group",
    "Undefined Treatment by Group",
    "Report Technique",
    "Vulnerabilities by assignment",
    "Status of assigned vulnerabilities",
    "Accepted vulnerabilities by severity",
    "Exposure by assignment",
    "Files with open vulnerabilities in the last 20 weeks",
    "Mean (average) days to remediate",
    "Groups availability",
    "Days since groups are failing",
    "Tags by groups",
]


def test_org_analytics(
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

    driver.get(
        f"{asm_endpoint}/graphics-for-organization?reportMode=true&"
        "bgChange=true&organization=ORG%2333c08ebd-2068-47e7-9673-e1aa03dc9448"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphics-for-group?reportMode=true&"
        "bgChange=true&group=unittesting"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphics-for-portfolio?reportMode=true&"
        "bgChange=true&portfolio=ORG%2338eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
        "PORTFOLIO%23test-groups"
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
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    # Login
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )

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
    try:
        close_tour = utils.wait_for_aria_label_by_parent(
            driver=driver,
            parent_id="react-joyride-step-0",
            parent_element="div",
            element="button",
            text="Skip",
            timeout=timeout,
        )
        close_tour.click()
        add_group.click()
    except TimeoutException:
        pass
    name = utils.wait_for_id(driver, "add-group-name", timeout)
    name.send_keys(group_name)
    description = utils.wait_for_id(driver, "add-group-description", timeout)
    description.send_keys(group_description)
    proceed = utils.wait_for_id(
        driver,
        "add-group-confirm",
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        "Group created successfully",
        timeout,
    )


def test_org_stakeholder(
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

    driver.get(f"{asm_endpoint}/orgs/okada/stakeholders")
    utils.wait_for_text(
        driver,
        "forces.unittesting@fluidattacks.com",
        timeout,
    )
    assert "First login" in driver.page_source


def test_org_portfolios(
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
