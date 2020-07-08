# Standard library
import asyncio
import contextlib
import os
import time
import socket
from typing import (
    Iterator,
)
from urllib.parse import quote_plus

# Third party libraries
import aiohttp
from backend.utils import (
    aio,
)
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)

# Local libraries
from analytics import (
    utils,
)

# Environment
GECKO = os.environ['pkgGeckoDriver']
FIREFOX = os.environ['pkgFirefox']

# Finding bugs?
DEBUGGING: bool = False

# Constants
INTEGRATES_API_TOKEN: str = os.environ['INTEGRATES_API_TOKEN']
PROXY = 'http://127.0.0.1:9000' if DEBUGGING else None
WIDTH: int = 1000


@contextlib.asynccontextmanager
async def selenium_web_driver() -> Iterator[webdriver.Firefox]:

    def create():
        options = Options()
        options.add_argument(f'--width={WIDTH}')
        options.add_argument('--height=64')
        options.headless = True

        driver: webdriver.Firefox = webdriver.Firefox(
            executable_path=f'{GECKO}/bin/geckodriver',
            firefox_binary=f'{FIREFOX}/bin/firefox',
            options=options,
        )

        return driver

    yield await aio.ensure_io_bound(create)


@contextlib.asynccontextmanager
async def http_session() -> Iterator[aiohttp.ClientSession]:
    connector = aiohttp.TCPConnector(
        ssl=False,
    )
    cookie_jar = aiohttp.CookieJar(
        unsafe=True,
    )
    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=None,
        sock_connect=None,
        sock_read=None,
    )

    async with aiohttp.ClientSession(
        connector=connector,
        cookie_jar=cookie_jar,
        timeout=timeout,
    ) as session:
        yield session


@aio.to_async
@utils.retry_on_exceptions(
    default_value=None,
    exceptions=(
        TimeoutException,
        WebDriverException,
    ),
    retry_times=5,
)
def take_snapshot(
    driver: webdriver.Firefox,
    save_as: str,
    session: aiohttp.ClientSession,
    url: str,
) -> None:
    driver.get(url)
    time.sleep(1)

    for cookie in session.cookie_jar:
        driver.add_cookie({'name': cookie.key, 'value': cookie.value})

    driver.get(url)
    time.sleep(10)

    element = driver.find_element_by_tag_name('body')
    with open(save_as, 'wb') as file:
        file.write(element.screenshot_as_png)


@utils.retry_on_exceptions(
    default_value=bytes(),
    exceptions=(
        aiohttp.ClientError,
        aiohttp.ClientOSError,
        socket.gaierror,
    ),
    retry_times=5,
)
async def insert_cookies(session: aiohttp.ClientSession) -> None:
    await session.get(
        headers={
            'Authorization': f'Bearer {INTEGRATES_API_TOKEN}'
        },
        proxy=PROXY,
        url='https://fluidattacks.com/integrates/graphics-for-group',
    )


async def main():
    async with http_session() as session, selenium_web_driver() as driver:
        base: str = 'https://fluidattacks.com/integrates/graphics-for-group'
        for group in map(quote_plus, utils.iterate_groups()):
            await insert_cookies(session)
            await take_snapshot(
                driver=driver,
                save_as=f'analytics/collector/graphics-for-group/{group}.png',
                session=session,
                url=f'{base}?group={group}&reportMode=true',
            )


if __name__ == '__main__':
    asyncio.run(main())
