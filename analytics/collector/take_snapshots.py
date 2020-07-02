# Standard library
import contextlib
from glob import glob
import os
import time
from typing import (
    Iterator,
)

# Third party libraries
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)

# Local libraries
from analytics.utils import (
    retry_on_exceptions,
)

# Environment
GECKO = os.environ['pkgGeckoDriver']
FIREFOX = os.environ['pkgFirefox']


@contextlib.contextmanager
def selenium_web_driver() -> Iterator[webdriver.Firefox]:
    options = Options()
    options.add_argument('--width=1360')
    options.add_argument('--height=768')
    options.binary_location = FIREFOX
    options.headless = True

    driver: webdriver.Firefox = webdriver.Firefox(
        executable_path=f'{GECKO}/bin/geckodriver',
        firefox_binary=f'{FIREFOX}/bin/firefox',
        options=options,
    )

    yield driver


@retry_on_exceptions(
    default_value=None,
    exceptions=(
        TimeoutException,
        WebDriverException,
    ),
    retry_times=5,
)
def take_snapshot(
    driver: webdriver.Firefox,
    url: str,
    width: int, height: int,
    save_to: str,
) -> None:
    driver.get(url)
    time.sleep(1.0)

    driver.save_screenshot(save_to)

    image = Image.open(save_to)
    image = image.crop((0, 0, width, height))
    image.save(save_to)


def main():
    htmls = sorted(glob('analytics/collector/**/*.html', recursive=True))

    with selenium_web_driver() as driver:
        for html in htmls:
            print(f'[INFO] Processing: {html}')

            path = os.path.abspath(html)
            name, _ = os.path.splitext(os.path.basename(path))
            width, height = name.split('x')

            take_snapshot(
                driver=driver,
                url=f'file://{path}',
                width=int(width),
                height=int(height),
                save_to=f'{html}.png',
            )


if __name__ == '__main__':
    main()
