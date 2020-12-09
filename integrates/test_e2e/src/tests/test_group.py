# Standard libraries
from random import randint

# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

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
    assert utils.wait_for_text(
        driver,
        'Now we can post comments on projects',
        timeout,
    )


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
    assert utils.wait_for_text(
        driver,
        'Reports are created on-demand',
        timeout,
    )


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
    assert utils.wait_for_text(
        driver,
        'unittest@fluidattacks.com',
        timeout,
    )


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
    assert utils.wait_for_text(
        driver,
        'Vulnerabilities over time',
        timeout,
    )


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
    assert utils.wait_for_text(
        driver,
        'title: FIN.S.0007. Cross site request forgery',
        timeout,
    )


def test_group_scope_repositories(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Add repo
    repo_name: str = f'test-repo-{randint(0, 1000)}'
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    add_repo = utils.wait_for_id(
        driver,
        'repository-add',
        timeout,
    )
    add_repo.click()
    name = utils.wait_for_name(
        driver,
        'resources[0].urlRepo',
        timeout
    )
    branch = utils.wait_for_name(
        driver,
        'resources[0].branch',
        timeout,
    )
    protocol = Select(utils.wait_for_name(
        driver,
        'resources[0].protocol',
        timeout,
    ))
    name.send_keys(repo_name)
    branch.send_keys('master')
    protocol.select_by_value('HTTPS')
    proceed = utils.wait_for_id(
        driver,
        'repository-add-proceed',
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        repo_name,
        timeout,
    )


def test_group_scope_environments(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Add environment
    environment_name: str = f'test-environment-{randint(0, 1000)}'
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    add_environment = utils.wait_for_id(
        driver,
        'environment-add',
        timeout,
    )
    add_environment.click()
    environment = utils.wait_for_name(
        driver,
        'resources[0].urlEnv',
        timeout
    )
    environment.send_keys(environment_name)
    proceed = utils.wait_for_id(
        driver,
        'environment-add-proceed',
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        environment_name,
        timeout,
    )


def test_group_scope_files(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter Scope
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    assert utils.wait_for_text(
        driver,
        'test.zip',
        timeout,
    )
