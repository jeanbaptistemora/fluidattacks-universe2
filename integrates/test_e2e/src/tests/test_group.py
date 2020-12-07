# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_group_consulting(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter group consulting
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/consulting')
    utils.wait_for_text(
        driver,
        'Now we can post comments on projects',
        timeout,
    )
    assert 'Now we can post comments on projects' in driver.page_source


def test_group_reports(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter reports
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    reports = utils.wait_for_id(
        driver,
        'reports',
        timeout,
    )
    reports.click()
    utils.wait_for_text(
        driver,
        'Reports are created on-demand',
        timeout,
    )
    assert 'Reports are created on-demand' in driver.page_source


def test_group_events(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter event
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/events')
    event = utils.wait_for_text(
        driver,
        'This is an eventuality with evidence',
        timeout,
    )
    event.click()
    utils.wait_for_text(
        driver,
        'unittest@fluidattacks.com',
        timeout,
    )
    assert 'unittest@fluidattacks.com' in driver.page_source


def test_group_analytics(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter Analytics
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/analytics')
    utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )
    assert 'Vulnerabilities over time' in driver.page_source


def test_group_forces(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter execution summary
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/devsecops')
    execution = utils.wait_for_text(
        driver,
        '08c1e735a73243f2ab1ee0757041f80e',
        timeout,
    )
    execution.click()
    utils.wait_for_text(
        driver,
        'unable to retrieve',
        timeout,
    )
    utils.wait_for_text(
        driver,
        'path/to/file2.ext',
        timeout,
    )
    assert 'unable to retrieve' in driver.page_source
    assert 'path/to/file2.ext' in driver.page_source

    # Enter execution log
    log = utils.wait_for_id(
        driver,
        'forcesExecutionLogTab',
        timeout,
    )
    log.click()
    utils.wait_for_text(
        driver,
        'title: FIN.S.0007. Cross site request forgery',
        timeout,
    )
    assert 'title: FIN.S.0007. Cross site request forgery' \
        in driver.page_source
