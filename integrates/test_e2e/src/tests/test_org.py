# Standard libraries
from typing import List

# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_org_analytics(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter Analytics
    driver.get(
        f'{integrates_endpoint}/orgs/okada/analytics')
    assert utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )


def test_org_groups(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Add group
    group_description: str = 'test-group-description'
    driver.get(f'{integrates_endpoint}/orgs/okada/groups')
    add_group = utils.wait_for_id(
        driver,
        'add-group',
        timeout,
    )
    add_group.click()
    description = utils.wait_for_id(
        driver,
        'add-group-description',
        timeout
    )
    description.send_keys(group_description)
    proceed = utils.wait_for_id(
        driver,
        'add-group-proceed',
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        'Group created successfully',
        timeout,
    )


def test_org_portfolios(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    expected_charts: List[str] = [
        'How many vulnerabilities are remediated (closed)?',
        'How many vulnerabilities are remediated and accepted?',
        'Findings by group',
        'Open findings by group',
        'Vulnerabilities status',
        'Vulnerabilities treatment',
        'Vulnerabilities by group',
        'Open vulnerabilities by group',
        'Mean (average) days to remediate',
        'Treatmentless by group',
        'Severity',
        'Days since last remediation',
        'Mean time to remediate',
    ]
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter portfolio
    driver.get(f'{integrates_endpoint}/orgs/okada/portfolios')
    test_projects = utils.wait_for_text(
        driver,
        'test-projects',
        timeout,
    )
    test_projects.click()
    for expected_chart in expected_charts:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )
