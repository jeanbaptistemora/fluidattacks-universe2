from model import (  # pylint: disable=import-error
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
import utils


def test_finding_description(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Enter finding description
    description = utils.wait_for_id(
        driver,
        "infoItem",
        timeout,
    )
    description.click()
    assert utils.wait_for_text(
        driver,
        "R359. Avoid using generic exceptions.",
        timeout,
    )


def test_finding_comments(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Enter finding comments
    comments = utils.wait_for_id(
        driver,
        "commentItem",
        timeout,
    )
    comments.click()
    assert utils.wait_for_text(
        driver,
        "This is a comenting test",
        timeout,
    )

    # Enter finding consulting not access
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/oneshottest/vulns")
    assert utils.wait_for_text(
        driver,
        "F037. Fuga de información técnica",
        timeout,
    )
    driver.get(
        f"{integrates_endpoint}/orgs/okada/groups/oneshottest/"
        "vulns/457497318/consulting"
    )
    assert utils.wait_for_text(
        driver,
        "Access denied",
        timeout,
    )

    # Enter finding observation
    driver.get(
        f"{integrates_endpoint}/orgs/okada/groups/oneshottest/"
        "vulns/457497318/observations"
    )
    assert utils.wait_for_text(
        driver,
        "No comments",
        timeout,
    )


def test_finding_evidence(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Enter finding evidences
    evidences = utils.wait_for_id(
        driver,
        "evidenceItem",
        timeout,
    )
    evidences.click()
    assert utils.wait_for_text(
        driver,
        "exception",
        timeout,
    )


def test_finding_severity(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Enter finding severity
    severity = utils.wait_for_id(
        driver,
        "cssv2Item",
        timeout,
    )
    severity.click()
    assert utils.wait_for_text(
        driver,
        "Confidentiality Impact",
        timeout,
    )


def test_finding_tracking(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Enter finding tracking
    tracking = utils.wait_for_id(
        driver,
        "trackingItem",
        timeout,
    )
    tracking.click()
    assert utils.wait_for_text(
        driver,
        "2020-01-03",
        timeout,
    )


def test_finding_reattack(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F014. Funcionalidad insegura",
        timeout,
    )
    finding.click()

    # Reattack all vulnerabilities
    start_reattack = utils.wait_for_id(
        driver,
        "start-reattack",
        timeout,
    )
    assert utils.wait_for_class_name(
        driver,
        "bg-lbl-red",
        timeout,
    )
    assert utils.wait_for_class_name(
        driver,
        "bg-lbl-green",
        timeout,
    )
    start_reattack.click()

    # hide closed vulnerabilities
    assert utils.wait_for_hide_class_name(
        driver,
        "bg-lbl-green",
        timeout,
    )
    assert utils.wait_for_class_name(
        driver,
        "bg-lbl-red",
        timeout,
    )

    checkboxes = driver.find_elements_by_css_selector(
        "#vulnerabilitiesTable input[type='checkbox']"
    )
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    confirm_reattack = utils.wait_for_id(
        driver,
        "confirm-reattack",
        timeout,
    )
    confirm_reattack.click()

    # Cancel reattack
    treatment = utils.wait_for_name(
        driver,
        "treatmentJustification",
        timeout,
    )
    cancel_reattack = utils.wait_for_id(
        driver,
        "cancel-remediation",
        timeout,
    )
    assert "Which was the applied solution?" in driver.page_source
    treatment.send_keys("test-justification")
    cancel_reattack.click()

    # show closed vulnerabilities again
    cancel_reattack.click()
    utils.wait_for_hide_text(
        driver,
        "Justification",
        timeout,
    )
    start_reattack.click()
    assert utils.wait_for_class_name(
        driver,
        "bg-lbl-green",
        timeout,
    )
    assert utils.wait_for_class_name(
        driver,
        "bg-lbl-red",
        timeout,
    )


def test_finding_vulnerabilities(
    driver: WebDriver,
    credentials: Credentials,
    integrates_endpoint: str,
    timeout: int,
) -> None:
    # Login
    utils.login(driver, integrates_endpoint, credentials)

    # Enter finding
    driver.get(f"{integrates_endpoint}/orgs/okada/groups/unittesting/vulns")
    finding = utils.wait_for_text(
        driver,
        "F060. Insecure exceptions",
        timeout,
    )
    finding.click()

    # Display Modal
    table_row = utils.wait_for_text(
        driver,
        "test/data/lib_path/f060/csharp.cs",
        timeout,
    )
    table_row.click()
    assert utils.wait_for_text(
        driver,
        "Vulnerability",
        timeout,
    )
    assert "Expiration" in driver.page_source
    close = utils.wait_for_id(
        driver,
        "close-vuln-modal",
        timeout,
    )
    close.click()
    assert utils.wait_for_hide_text(
        driver,
        "Vulnerability",
        timeout,
    )

    # Edit vulnerabilities
    edit_vulns = utils.wait_for_id(
        driver,
        "vulnerabilities-edit",
        timeout,
    )
    edit_vulns.click()
    checkboxes = driver.find_elements_by_css_selector(
        "#vulnerabilitiesTable input[type='checkbox']"
    )
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    assert "test/data/lib_path/f060/csharp.cs" in driver.page_source
    edit_vulns.click()
