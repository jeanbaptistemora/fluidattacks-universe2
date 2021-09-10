from aioextensions import (
    collect,
    CPU_CORES,
)
import bs4
from datetime import (
    datetime,
)
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
from queue import (
    SimpleQueue,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)
import urllib.parse
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
    get_offset,
)

CHECKS: Tuple[
    Tuple[
        Callable[[URLContext], Any],
        Dict[
            core_model.FindingEnum,
            List[Callable[[Any], core_model.Vulnerabilities]],
        ],
    ],
    ...,
] = (
    (analyze_content.get_check_ctx, analyze_content.CHECKS),
    (analyze_headers.get_check_ctx, analyze_headers.CHECKS),
)


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    url: URLContext,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    unique_count: int,
) -> None:
    await log("info", "Analyzing http %s of %s: %s", index, unique_count, url)

    for get_check_ctx, checks in CHECKS:
        for finding, check_list in checks.items():
            if finding in CTX.config.checks:
                for check in check_list:
                    for vuln in check(get_check_ctx(url)):
                        await stores[vuln.finding].store(vuln)


@rate_limited(rpm=LIB_HTTP_DEFAULT)
async def get_url(
    url: str,
    *,
    ntp_offset: Optional[float],
) -> Optional[URLContext]:
    async with create_session() as session:
        if response := await request(session, "GET", url):
            url = str(response.url)  # Update with the redirected URL

            content_raw = await response.content.read(1048576)
            content = content_raw.decode("latin-1")
            soup = bs4.BeautifulSoup(content, features="html.parser")

            return URLContext(
                components=urllib.parse.urlparse(url),
                content=content,
                custom_f023=await request(
                    session,
                    "GET",
                    url,
                    headers={
                        "Host": "fluidattacks.com",
                    },
                ),
                headers_raw=response.headers,
                is_html=is_html(content, soup),
                soup=soup,
                timestamp_ntp=(
                    datetime.now().timestamp() + ntp_offset
                    if ntp_offset
                    else None
                ),
                url=url,
            )

    return None


async def get_urls() -> Set[URLContext]:
    urls: Set[URLContext] = set()
    urls_done: Set[str] = set()
    urls_pending: SimpleQueue = SimpleQueue()

    ntp_offset: Optional[float] = get_offset()

    for url in set(CTX.config.http.include):
        urls_pending.put(url)

    while not urls_pending.empty():
        url = urls_pending.get()
        url_ctx: Optional[URLContext] = await get_url(
            url,
            ntp_offset=ntp_offset,
        )
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
    if not any(
        finding in CTX.config.checks
        for _, checks in CHECKS
        for finding in checks
    ):
        return

    unique_urls: Set[URLContext] = await get_urls()
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
