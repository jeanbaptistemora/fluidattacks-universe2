# Standard library
from queue import (
    SimpleQueue,
)
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
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
from html_ import (
    get_sameorigin_urls,
    is_html,
)
from lib_http import (
    analyze_content,
    analyze_headers,
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
from utils.ntp import (
    get_ntp_now,
)


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    url: URLContext,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    unique_count: int,
) -> None:
    checks: Dict[
        core_model.FindingEnum,
        Callable[[Any], core_model.Vulnerabilities],
    ]

    await log("info", "Analyzing http %s of %s: %s", index, unique_count, url)

    for get_check_ctx, checks in (  # type: ignore
        (analyze_content.get_check_ctx, analyze_content.CHECKS),
        (analyze_headers.get_check_ctx, analyze_headers.CHECKS),
    ):
        for finding, check in checks.items():
            if finding in CTX.config.checks:
                for vulnerability in check(get_check_ctx(url)):
                    await stores[vulnerability.finding].store(vulnerability)


def should_include_url(url: URLContext) -> bool:
    if url.components.netloc in {
        "play.google.com",
        "www.getpostman.com",
    }:
        log_blocking("warn", "Ignoring lib_http checks over: %s", url)
        return False

    return True


@rate_limited(rpm=LIB_HTTP_DEFAULT)
async def get_url(url: str) -> Optional[URLContext]:
    async with create_session() as session:
        if response := await request(session, "GET", url):
            content_raw = await response.content.read(1048576)
            content = content_raw.decode("latin-1")
            soup = bs4.BeautifulSoup(content, features="html.parser")

            return URLContext(
                components=urllib.parse.urlparse(url),
                content=content,
                headers_raw=response.headers,
                is_html=is_html(content, soup),
                soup=soup,
                timestamp_ntp=get_ntp_now(),
                url=url,
            )

    return None


async def get_urls() -> Set[URLContext]:
    urls: Set[URLContext] = set()
    urls_done: Set[str] = set()
    urls_pending: SimpleQueue = SimpleQueue()

    for url in set(CTX.config.http.include):
        urls_pending.put(url)

    while not urls_pending.empty():
        url = urls_pending.get()
        url_ctx: Optional[URLContext] = await get_url(url)
        if url_ctx is None:
            continue

        urls.add(url_ctx)
        urls_done.add(url)

        for child_url in get_sameorigin_urls(url_ctx.components, url_ctx.soup):
            if child_url not in urls_done:
                log_blocking("info", "Discovered url: %s", child_url)
                urls_pending.put(child_url)

    return urls


async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    unique_urls: Set[URLContext] = await get_urls()
    unique_urls = set(filter(should_include_url, unique_urls))
    unique_count: int = len(unique_urls)

    await collect(
        (
            analyze_one(
                index=index,
                url=url,
                stores=stores,
                unique_count=unique_count,
            )
            for index, url in enumerate(unique_urls)
        ),
        workers=CPU_CORES,
    )
