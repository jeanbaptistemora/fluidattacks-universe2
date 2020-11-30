# Standard libraries
from typing import Any, Dict

# Third party libraries
from selenium import webdriver

# Local libraries
import conftest

def test_login_screen() -> None:
    desired_cap: Dict[str,str] = conftest.BROWSERSTACK_DESIRED_CAP
    desired_cap['name'] = test_login_screen.__name__

    driver: Any = webdriver.Remote(
        command_executor=conftest.BROWSERSTACK_URL,
        desired_capabilities=desired_cap
    )

    driver.get(conftest.URL)
    assert 'Integrates | Fluid Attacks' in driver.title
    driver.quit()

test_login_screen()
