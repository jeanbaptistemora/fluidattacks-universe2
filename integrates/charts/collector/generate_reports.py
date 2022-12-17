from aioextensions import (
    in_thread,
    run,
)
import aiohttp
import asyncio
from charts import (
    utils,
)
import contextlib
from decorators import (
    retry_on_exceptions,
)
from newutils.encodings import (
    safe_encode,
)
import os
from selenium import (
    webdriver,
)
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import (
    By,
)
from selenium.webdriver.firefox.options import (
    Options,
)
from selenium.webdriver.support import (
    expected_conditions as ec,
)
from selenium.webdriver.support.wait import (
    WebDriverWait,
)
import socket
from typing import (
    AsyncIterator,
)
from urllib.parse import (
    quote_plus as percent_encode,
)

# Environment
GECKO = os.environ["envGeckoDriver"]
FIREFOX = os.environ["envFirefox"]

# Finding bugs?
DEBUGGING: bool = False

# Constants
TARGET_URL: str = "https://app.fluidattacks.com"
INTEGRATES_API_TOKEN: str = os.environ["INTEGRATES_API_TOKEN"]
PROXY = "http://127.0.0.1:9000" if DEBUGGING else None
COOKIE_MESSAGE = "Allow all cookies"
WIDTH: int = 1200


@contextlib.asynccontextmanager
async def selenium_web_driver() -> AsyncIterator[webdriver.Firefox]:
    def create() -> webdriver.Firefox:
        options = Options()
        options.add_argument(f"--width={WIDTH}")
        options.add_argument("--height=800")
        options.headless = True

        driver: webdriver.Firefox = webdriver.Firefox(
            executable_path=f"{GECKO}/bin/geckodriver",
            firefox_binary=f"{FIREFOX}/bin/firefox",
            options=options,
        )

        return driver

    # Exception: WF(AsyncIterator is subtype of iterator)
    yield await in_thread(create)  # NOSONAR


@contextlib.asynccontextmanager
async def http_session() -> AsyncIterator[aiohttp.ClientSession]:
    connector = aiohttp.TCPConnector()
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
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield session  # NOSONAR


@retry_on_exceptions(
    exceptions=(
        NoSuchElementException,
        TimeoutException,
        WebDriverException,
    ),
    max_attempts=5,
    sleep_seconds=float("1.0"),
)
async def take_snapshot(  # pylint: disable=too-many-arguments
    driver: webdriver.Firefox,
    save_as: str,
    session: aiohttp.ClientSession,
    url: str,
    entity: str,
    subject: str = "*",
) -> None:
    await insert_cookies(entity, session, subject)
    driver.get(TARGET_URL)
    await asyncio.sleep(1)

    with contextlib.suppress(NoSuchElementException):
        if driver.find_element(
            By.XPATH,
            f"//*[text()[contains(., '{COOKIE_MESSAGE}')]]",
        ):
            allow_cookies = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[text()[contains(., '{COOKIE_MESSAGE}')]]",
                    )
                )
            )
            allow_cookies.click()
            await asyncio.sleep(2)

    for cookie in session.cookie_jar:
        driver.add_cookie({"name": cookie.key, "value": cookie.value})

    await asyncio.sleep(1)
    driver.get(url)
    await asyncio.sleep(10)
    if not WebDriverWait(driver, 20).until(
        ec.presence_of_element_located(
            (
                By.ID,
                "root",
            )
        )
    ):
        raise TimeoutException()

    with contextlib.suppress(NoSuchElementException):
        if driver.find_element(
            By.XPATH,
            "//*[text()[contains(., 'Error code')]]",
        ):
            raise TimeoutException()

    if WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "report-title-pad"))
    ):
        with open(save_as, "wb") as file:
            scroll_width = driver.execute_script(
                "return document.body.parentNode.scrollWidth"
            )
            scroll_height = driver.execute_script(
                "return document.body.parentNode.scrollHeight"
            )
            driver.set_window_size(scroll_width, scroll_height)
            file.write(driver.get_full_page_screenshot_as_png())


@retry_on_exceptions(
    exceptions=(
        TimeoutException,
        WebDriverException,
    ),
    max_attempts=5,
    sleep_seconds=float("1.0"),
)
async def clear_cookies(
    driver: webdriver.Firefox,
    session: aiohttp.ClientSession,
) -> None:
    driver.get(f"{TARGET_URL}/logout")
    session.cookie_jar.clear()
    driver.delete_all_cookies()
    await asyncio.sleep(1)


@retry_on_exceptions(
    exceptions=(
        aiohttp.ClientError,
        aiohttp.ClientOSError,
        socket.gaierror,
    ),
    max_attempts=5,
    sleep_seconds=float("1.0"),
)
async def insert_cookies(
    entity: str, session: aiohttp.ClientSession, subject: str = "*"
) -> None:
    await session.get(
        headers={"Authorization": f"Bearer {INTEGRATES_API_TOKEN}"},
        proxy=PROXY,
        url=f"{TARGET_URL}/graphics-for-{entity}?{entity}={subject}",
    )


async def main() -> None:
    base: str

    async with http_session() as session, selenium_web_driver() as driver:

        # Organization reports
        base = (
            f"{TARGET_URL}/graphics-for-organization?"
            f"reportMode=true&bgChange=true"
        )
        async for org_id, _, _ in utils.iterate_organizations_and_groups():
            await take_snapshot(
                driver=driver,
                save_as=utils.get_result_path(
                    name=f"organization:{safe_encode(org_id.lower())}.png",
                ),
                session=session,
                url=f"{base}&organization={percent_encode(org_id)}",
                entity="organization",
            )
            await clear_cookies(driver, session)

        # Group reports
        base = (
            f"{TARGET_URL}/graphics-for-group?"
            f"reportMode=true&bgChange=true"
        )
        async for group in utils.iterate_groups():
            await take_snapshot(
                driver=driver,
                save_as=utils.get_result_path(
                    name=f"group:{safe_encode(group.lower())}.png",
                ),
                session=session,
                url=f"{base}&group={percent_encode(group)}",
                entity="group",
            )
            await clear_cookies(driver, session)

        # Portfolio reports
        base = (
            f"{TARGET_URL}/graphics-for-portfolio?"
            f"reportMode=true&bgChange=true"
        )
        separator = "PORTFOLIO#"
        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, _ in await utils.get_portfolios_groups(org_name):
                subject = percent_encode(org_id + separator + portfolio)
                await take_snapshot(
                    driver=driver,
                    save_as=utils.get_result_path(
                        name="portfolio:"
                        + safe_encode(
                            org_id.lower()
                            + separator.lower()
                            + portfolio.lower()
                        )
                        + ".png",
                    ),
                    session=session,
                    url=f"{base}&portfolio={subject}",
                    entity="portfolio",
                    subject=subject,
                )
                await clear_cookies(driver, session)


if __name__ == "__main__":
    run(main())
