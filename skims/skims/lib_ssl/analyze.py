from aioextensions import (
    collect,
    CPU_CORES,
)
from collections.abc import (
    Callable,
)
from contextlib import (
    suppress,
)
from ctx import (
    CTX,
)
from lib_ssl import (
    analyze_protocol,
)
from lib_ssl.suites import (
    SSLVersionId,
)
from lib_ssl.types import (
    SSLContext,
    SSLServerResponse,
)
from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
from urllib3 import (
    exceptions,
)
from urllib3.util.url import (
    parse_url,
)
from utils.function import (
    shield,
)
from utils.logs import (
    log,
)

CHECKS: tuple[
    dict[
        core_model.FindingEnum,
        list[Callable[[Any], core_model.Vulnerabilities]],
    ],
    ...,
] = (analyze_protocol.CHECKS,)


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    ssl_ctx: SSLContext,
    stores: dict[core_model.FindingEnum, EphemeralStore],
    count: int,
) -> None:
    await log("info", "Analyzing ssl %s of %s: %s", index, count, ssl_ctx)

    for checks in CHECKS:
        for finding, check_list in checks.items():
            if finding in CTX.config.checks:
                for check in check_list:
                    for vulnerability in check(ssl_ctx):
                        stores[vulnerability.finding].store(vulnerability)


def _get_ssl_targets(urls: set[str]) -> set[tuple[str, int]]:
    targets: set[tuple[str, int]] = set()
    default_port = 443
    for url in urls:
        with suppress(ValueError, exceptions.HTTPError):
            parsed_url = parse_url(url)
            if not parsed_url.host:
                continue

            if parsed_url.port is None:
                targets.add((parsed_url.host, default_port))
            else:
                targets.add((parsed_url.host, parsed_url.port))

    return targets


def _get_ssl_context(host: str, port: int) -> SSLContext:
    responses: list[SSLServerResponse] = []
    for v_id in SSLVersionId:
        with suppress(Exception):
            if v_id != SSLVersionId.sslv3_0 and (
                tls_response := analyze_protocol.tls_connect(
                    host=host,
                    port=port,
                    v_id=v_id,
                )
            ):
                responses = [*responses, tls_response]

    return SSLContext(
        host=host,
        port=port,
        tls_responses=tuple(responses),
    )


async def get_ssl_contexts() -> set[SSLContext]:
    ssl_contexts: set[SSLContext] = set()
    for target in CTX.config.dast.ssl.include:
        ssl_contexts.add(_get_ssl_context(target.host, target.port))

    if CTX.config.dast.ssl_checks:
        for host, port in _get_ssl_targets(set(CTX.config.dast.urls)):
            ssl_contexts.add(_get_ssl_context(host, port))

    return ssl_contexts


async def analyze(
    *,
    stores: dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in CTX.config.checks for checks in CHECKS for finding in checks
    ):
        return

    unique_ssl_contexts: set[SSLContext] = await get_ssl_contexts()
    count: int = len(unique_ssl_contexts)

    await collect(
        (
            analyze_one(
                index=index,
                ssl_ctx=ssl_ctx,
                stores=stores,
                count=count,
            )
            for index, ssl_ctx in enumerate(unique_ssl_contexts, start=1)
        ),
        workers=CPU_CORES,
    )
