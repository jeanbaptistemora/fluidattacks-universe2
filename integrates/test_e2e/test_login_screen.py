# Standard libraries
from typing import Any, Dict

# Third party libraries
from selenium import webdriver

def test_login_screen(browserstack_cap: Dict[str, str], browserstack_url: str, endpoint: str) -> None:
    browserstack_cap['name'] = test_login_screen.__name__

    driver: Any = webdriver.Remote(
        command_executor=browserstack_url,
        desired_capabilities=browserstack_cap
    )

    driver.get(endpoint)
    assert 'Integrates | Fluid Attacks' in driver.title
    driver.quit()
