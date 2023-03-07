import bs4
from collections.abc import (
    Callable,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from ctx import (
    CTX,
)
from datetime import (
    datetime,
)
from lib_http import (
    analyze_content,
    analyze_dns,
    analyze_headers,
)
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from more_itertools import (
    collapse,
)
from queue import (
    SimpleQueue,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
import urllib.parse
from utils.function import (
    shield_blocking,
)
from utils.html import (
    get_alternative_protocol_urls,
    get_sameorigin_urls,
    is_html,
)
from utils.http import (
    create_session,
    request,
)
from utils.logs import (
    log_blocking,
)
from utils.ntp import (
    get_offset,
)

CHECKS: tuple[
    tuple[
        Callable[[URLContext], Any],
        dict[
            core_model.FindingEnum,
            list[Callable[[Any], core_model.Vulnerabilities]],
        ],
    ],
    ...,
] = (
    (analyze_content.get_check_ctx, analyze_content.CHECKS),
    (analyze_dns.get_check_ctx, analyze_dns.CHECKS),
    (analyze_headers.get_check_ctx, analyze_headers.CHECKS),
)


@shield_blocking(on_error_return=[])
def analyze_one(
    *,
    index: int,
    url: URLContext,
    unique_count: int,
) -> tuple[core_model.Vulnerability, ...]:
    log_blocking(
        "info", "Analyzing http %s of %s: %s", index, unique_count, url
    )
    vulns: tuple[core_model.Vulnerability, ...] = tuple()

    for get_check_ctx, checks in CHECKS:
        url_ctx = get_check_ctx(url)
        for finding, check_list in checks.items():
            if (
                finding not in CTX.config.checks
                or (
                    url.response_status >= 400
                    and finding is not core_model.FindingEnum.F015
                )
                or (
                    url.response_status != 401
                    and finding is core_model.FindingEnum.F015
                )
            ):
                continue

            for check in check_list:
                vulns += check(url_ctx)

    return vulns


# @rate_limited(rpm=LIB_HTTP_DEFAULT)
async def get_url(
    url: str,
    *,
    ntp_offset: float | None,
) -> URLContext | None:
    # Urls for common attached file extensions should be excluded from analysis
    ignored_ext = (
        "css",
        "js",
        "jpg",
        "jpeg",
        "png",
    )
    if url.endswith(ignored_ext):
        return None

    async with create_session() as session:  # type: ignore
        if response := await request(session, "GET", url):
            redirect_url = str(response.url)  # Update with the redirected URL
            has_redirect: bool = redirect_url != url
            if not url.endswith("/") and redirect_url == f"{url}/":
                has_redirect = False

            content_raw = await response.content.read(1048576)
            content = content_raw.decode("latin-1")
            soup = bs4.BeautifulSoup(content, features="html.parser")

            return URLContext(
                components=urllib.parse.urlparse(redirect_url),
                content=content,
                custom_f023=await request(
                    session,
                    "GET",
                    url,
                    headers={
                        "Host": "fluidattacks.com",
                    },
                ),
                has_redirect=has_redirect,
                headers_raw=response.headers,  # type: ignore
                is_html=is_html(content, soup),
                original_url=url,
                soup=soup,
                timestamp_ntp=(
                    datetime.now().timestamp() + ntp_offset
                    if ntp_offset
                    else None
                ),
                url=redirect_url,
                response_status=response.status,
            )

    return None


async def get_urls() -> set[URLContext]:
    urls: set[URLContext] = set()
    urls_done: set[str] = set()
    urls_pending: SimpleQueue = SimpleQueue()
    ntp_offset: float | None = get_offset()

    for url in set(CTX.config.dast.http.include):
        urls_pending.put(url)

    if CTX.config.dast.http_checks:
        for url in get_alternative_protocol_urls(set(CTX.config.dast.urls)):
            urls_pending.put(url)

    while not urls_pending.empty():
        url = urls_pending.get()
        url_ctx: URLContext | None = await get_url(
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
    stores: dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in CTX.config.checks
        for _, checks in CHECKS
        for finding in checks
    ):
        return

    unique_urls: set[URLContext] = await get_urls()
    unique_count: int = len(unique_urls)

    with ThreadPoolExecutor() as executor:
        vulnerabilities: tuple[core_model.Vulnerability, ...] = tuple(
            collapse(
                (
                    analyze_one(
                        index=index,
                        url=url,
                        unique_count=unique_count,
                    )
                    for index, url in enumerate(unique_urls)
                ),
                base_type=core_model.Vulnerability,
            )
        )
        executor.map(
            lambda x: stores[  # pylint: disable=unnecessary-lambda
                x.finding
            ].store(x),
            vulnerabilities,
        )
