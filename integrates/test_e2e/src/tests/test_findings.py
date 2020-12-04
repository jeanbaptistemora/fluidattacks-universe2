# Third party libraries
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# Local libraries
import utils
from model import (
    AzureCredentials
)


def test_findings(
        driver: WebDriver,
        azure_credentials: AzureCredentials,
        integrates_endpoint: str,
        timeout: int) -> None:
    utils.login_azure(driver, azure_credentials, timeout)
    utils.login_integrates_azure(driver, integrates_endpoint, timeout)
    driver.get(f'{integrates_endpoint}/orgs/okada/groups/unittesting/vulns')
    WebDriverWait(driver, timeout).until(ec.presence_of_element_located((
        By.XPATH, "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]"
    )))
    assert 'FIN.H.060. Insecure exceptions' in driver.page_source
    driver.quit()
