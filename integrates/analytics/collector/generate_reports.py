# Standard library
import asyncio
import contextlib
import os
import time
import socket
from typing import (
    Iterator,
)
from urllib.parse import (
    quote_plus as percent_encode,
)

# Third party libraries
import aiohttp
from backend.utils import (
    aio,
)
from backend.utils.encodings import (
    safe_encode,
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
TARGET_URL: str = 'https://fluidattacks.com/integrates'
INTEGRATES_API_TOKEN: str = os.environ['INTEGRATES_API_TOKEN']
PROXY = 'http://127.0.0.1:9000' if DEBUGGING else None
WIDTH: int = 1200


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
async def insert_cookies(entity: str, session: aiohttp.ClientSession) -> None:
    await session.get(
        headers={
            'Authorization': f'Bearer {INTEGRATES_API_TOKEN}'
        },
        proxy=PROXY,
        url=f'{TARGET_URL}/graphics-for-{entity}?{entity}=*',
    )


async def main():
    base: str

    async with http_session() as session, selenium_web_driver() as driver:

        # Organization reports
        base = f'{TARGET_URL}/graphics-for-organization?reportMode=true'
        async for org_id, _, _ in utils.iterate_organizations_and_groups():
            await insert_cookies('organization', session)
            await take_snapshot(
                driver=driver,
                save_as=utils.get_result_path(
                    name=f'organization:{safe_encode(org_id.lower())}.png',
                ),
                session=session,
                url=f'{base}&organization={percent_encode(org_id)}',
            )

        # Group reports
        base = f'{TARGET_URL}/graphics-for-group?reportMode=true'
        async for group in utils.iterate_groups():
            await insert_cookies('group', session)
            await take_snapshot(
                driver=driver,
                save_as=utils.get_result_path(
                    name=f'group:{safe_encode(group.lower())}.png',
                ),
                session=session,
                url=f'{base}&group={percent_encode(group)}',
            )


if __name__ == '__main__':
    asyncio.run(main())
