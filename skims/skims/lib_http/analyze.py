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

# Local libraries
from lib_http import (
    f043,
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
from utils.limits import (
    LIB_HTTP_DEFAULT,
)
from utils.logs import (
    log,
    log_blocking,
)


@shield(on_error_return=[])
@rate_limited(rpm=LIB_HTTP_DEFAULT)
async def analyze_one(
    *,
    index: int,
    url: str,
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


def should_include_url(url: str) -> bool:
    components = urllib.parse.urlparse(url)

    if components.netloc == 'play.google.com':
        log_blocking('warn', 'Ignoring lib_http checks over: %s', url)
        return False

    return True


async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    unique_urls: Set[str] = set(CTX.config.http.include)
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
