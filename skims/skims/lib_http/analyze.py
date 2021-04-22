# Standard library
from typing import (
    Dict,
    Set,
)
import urllib.parse

# Third party libraries
from aioextensions import (
    CPU_CORES,
    collect,
)
import bs4

# Local libraries
from lib_http import (
    f043,
)
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ctx import (
    CTX,
)
from utils.function import (
    rate_limited,
    shield,
)
from utils.html import (
    is_html,
)
from utils.http import (
    create_session,
    request,
)
from utils.limits import (
    LIB_HTTP_DEFAULT,
)
from utils.logs import (
    log,
    log_blocking,
)


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    url: URLContext,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    unique_count: int,
) -> None:
    await log('info', 'Analyzing http %s of %s: %s', index, unique_count, url)

    for should_run, analyzer in (
        (f043.should_run, f043.analyze),
    ):
        if should_run():
            for vulnerabilities in analyzer(url):
                for vulnerability in await vulnerabilities:
                    await stores[vulnerability.finding].store(vulnerability)


def should_include_url(url: URLContext) -> bool:
    if url.components.netloc in {
        'play.google.com',
        'www.getpostman.com',
    }:
        log_blocking('warn', 'Ignoring lib_http checks over: %s', url)
        return False

    return True


@rate_limited(rpm=LIB_HTTP_DEFAULT)
async def get_url(url: str) -> URLContext:
    async with create_session() as session:
        response = await request(session, 'GET', url)
        content_raw = await response.content.read(1048576)
        content = content_raw.decode('latin-1')
        soup = bs4.BeautifulSoup(content)

        return URLContext(
            components=urllib.parse.urlparse(url),
            content=content,
            headers_raw=response.headers,
            is_html=is_html(content, soup),
            soup=soup,
            url=url,
        )


async def get_urls() -> Set[URLContext]:
    urls: Set[URLContext] = set()

    for url in set(CTX.config.http.include):
        urls.add(await get_url(url))

    return urls


async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    unique_urls: Set[URLContext] = await get_urls()
    unique_urls = set(filter(should_include_url, unique_urls))
    unique_count: int = len(unique_urls)

    await collect((
        analyze_one(
            index=index,
            url=url,
            stores=stores,
            unique_count=unique_count,
        )
        for index, url in enumerate(unique_urls)
    ), workers=CPU_CORES)
