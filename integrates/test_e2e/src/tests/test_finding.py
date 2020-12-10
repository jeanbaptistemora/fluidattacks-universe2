# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_finding_description(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding description
    description = utils.wait_for_id(
        driver,
        'infoItem',
        timeout,
    )
    description.click()
    assert utils.wait_for_text(
        driver,
        'R359. Avoid using generic exceptions.',
        timeout,
    )


def test_finding_comments(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding comments
    comments = utils.wait_for_id(
        driver,
        'commentItem',
        timeout,
    )
    comments.click()
    assert utils.wait_for_text(
        driver,
        'This is a comenting test',
        timeout,
    )


def test_finding_exploit(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding exploit
    exploit = utils.wait_for_id(
        driver,
        'exploitItem',
        timeout,
    )
    exploit.click()
    assert utils.wait_for_text(
        driver,
        'It works',
        timeout,
    )


def test_finding_evidence(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding evidences
    evidences = utils.wait_for_id(
        driver,
        'evidenceItem',
        timeout,
    )
    evidences.click()
    assert utils.wait_for_text(
        driver,
        'exception',
        timeout,
    )


def test_finding_severity(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding severity
    severity = utils.wait_for_id(
        driver,
        'cssv2Item',
        timeout,
    )
    severity.click()
    assert utils.wait_for_text(
        driver,
        'Confidentiality Impact',
        timeout,
    )


def test_finding_tracking(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Enter finding tracking
    tracking = utils.wait_for_id(
        driver,
        'trackingItem',
        timeout,
    )
    tracking.click()
    assert utils.wait_for_text(
        driver,
        '2020-09-09',
        timeout,
    )


def test_finding_reattack(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    # Login
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)

    # Enter finding
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    finding = utils.wait_for_text(
        driver,
        'FIN.H.060. Insecure exceptions',
        timeout,
    )
    finding.click()

    # Reattack all vulnerabilities
    start_reattack = utils.wait_for_id(
        driver,
        'start-reattack',
        timeout,
    )
    start_reattack.click()
    checkboxes = driver.find_elements_by_css_selector(
        "#linesVulns input[type='checkbox']")
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    confirm_reattack = utils.wait_for_id(
        driver,
        'confirm-reattack',
        timeout,
    )
    confirm_reattack.click()

    # Cancel reattack
    treatment = utils.wait_for_name(
        driver,
        'treatmentJustification',
        timeout,
    )
    cancel_reattack = utils.wait_for_id(
        driver,
        'cancel-remediation',
        timeout,
    )
    assert 'Which was the applied solution?' in driver.page_source
    treatment.send_keys('test-justification')
    cancel_reattack.click()
