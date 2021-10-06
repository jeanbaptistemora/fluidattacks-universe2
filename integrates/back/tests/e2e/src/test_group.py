from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
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
        "Now we can post comments on projects",
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
    assert utils.wait_for_text(
        driver,
        "Reports are created on-demand",
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
    # Login
    utils.login(driver, asm_endpoint, credentials)

    # Enter Analytics
    driver.get(f"{asm_endpoint}/orgs/okada/groups/unittesting/analytics")
    assert utils.wait_for_text(
        driver,
        "Severity over time",
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
    execution = utils.wait_for_text(
        driver,
        "08c1e735a73243f2ab1ee0757041f80e",
        timeout,
    )
    execution.click()
    utils.wait_for_text(
        driver,
        "unable to retrieve",
        timeout,
    )
    utils.wait_for_text(
        driver,
        "path/to/file2.ext",
        timeout,
    )
    assert "unable to retrieve" in driver.page_source
    assert "path/to/file2.ext" in driver.page_source

    # Enter execution log
    log = utils.wait_for_id(
        driver,
        "forcesExecutionLogTab",
        timeout,
    )
    log.click()
    assert utils.wait_for_text(
        driver,
        "Cross site request forgery",
        timeout,
    )


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

    environment = utils.wait_for_name(driver, "environmentUrls[0]", timeout)
    environment_name: str = utils.rand_name("https://test.fluidattacks.com")
    environment.clear()
    environment.send_keys(environment_name)
    proceed = utils.wait_for_id(
        driver,
        "envs-manage-proceed",
        timeout,
    )
    proceed.click()
    expand_button = utils.wait_for_class_name(
        driver, "expand-cell-header", timeout
    )
    expand_button.click()
    assert utils.wait_for_text(
        driver,
        environment_name,
        timeout,
    )


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
