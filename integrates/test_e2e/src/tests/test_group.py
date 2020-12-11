# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    Credentials
)


def test_group_consulting(
        driver: WebDriver,
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Add repo
    repo_url: str = utils.rand_name('https://gitlab.com/fluidattacks/test')
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    add_repo = utils.wait_for_id(
        driver,
        'git-root-add',
        timeout,
    )
    add_repo.click()
    url = utils.wait_for_name(
        driver,
        'url',
        timeout
    )
    branch = utils.wait_for_name(
        driver,
        'branch',
        timeout,
    )
    environment = utils.wait_for_name(
        driver,
        'environment',
        timeout,
    )
    url.send_keys(repo_url)
    branch.send_keys('master')
    environment.send_keys('production')
    proceed = utils.wait_for_id(
        driver,
        'git-root-add-proceed',
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
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Add environment
    environment_name: str = utils.rand_name('test-environment')
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
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter Scope
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    assert utils.wait_for_text(
        driver,
        'test.zip',
        timeout,
    )


def test_group_scope_portfolio(
        driver: WebDriver,
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Add tag
    tag_name: str = utils.rand_name('test-portfolio')
    driver.get(
        f'{integrates_endpoint}/orgs/okada/groups/unittesting/scope')
    add_tag = utils.wait_for_id(
        driver,
        'portfolio-add',
        timeout,
    )
    add_tag.click()
    tags = utils.wait_for_name(
        driver,
        'tags[0]',
        timeout
    )
    tags.send_keys(tag_name)
    proceed = utils.wait_for_id(
        driver,
        'portfolio-add-proceed',
        timeout,
    )
    proceed.click()
    assert utils.wait_for_text(
        driver,
        tag_name,
        timeout,
    )


def test_group_pending_to_delete(
        driver: WebDriver,
        credentials: Credentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    expected_text: str = 'Group pending to delete'
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter group home
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/pendingproject')
    assert utils.wait_for_text(
        driver,
        expected_text,
        timeout,
    )

    # Enter group vulnerabilities
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/pendingproject/vulns')
    assert utils.wait_for_text(
        driver,
        expected_text,
        timeout,
    )
