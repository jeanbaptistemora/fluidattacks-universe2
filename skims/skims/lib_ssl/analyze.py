from aioextensions import (
    collect,
    CPU_CORES,
)
from lib_ssl import (
    analyze_protocol,
)
from lib_ssl.suites import (
    SSLVersionId,
)
from lib_ssl.types import (
    SSLContext,
)
from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Set,
    Tuple,
)
from utils.ctx import (
    CTX,
)
from utils.function import (
    shield,
)
from utils.logs import (
    log,
)

CHECKS: Tuple[
    Dict[
        core_model.FindingEnum,
        List[Callable[[Any], core_model.Vulnerabilities]],
    ],
    ...,
] = (analyze_protocol.CHECKS,)


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    ssl_ctx: SSLContext,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    count: int,
) -> None:

    await log("info", "Analyzing ssl %s of %s: %s", index, count, ssl_ctx)

    for checks in CHECKS:
        for finding, check_list in checks.items():
            if finding in CTX.config.checks:
                for check in check_list:
                    for vulnerability in check(ssl_ctx):
                        stores[vulnerability.finding].store(vulnerability)


async def get_ssl_contexts() -> Set[SSLContext]:
    ssl_contexts: Set[SSLContext] = {
        SSLContext(
            host=target.host,
            port=target.port,
            tls_responses=tuple(
                tls_response
                for v_id in SSLVersionId
                if v_id != SSLVersionId.sslv3_0
                and (
                    tls_response := analyze_protocol.tls_connect(
                        host=target.host,
                        port=target.port,
                        v_id=v_id,
                    )
                )
            ),
        )
        for target in CTX.config.ssl.include
    }

    return ssl_contexts


async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:

    if not any(
        finding in CTX.config.checks for checks in CHECKS for finding in checks
    ):
        return

    unique_ssl_contexts: Set[SSLContext] = await get_ssl_contexts()
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
