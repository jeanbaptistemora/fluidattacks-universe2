from aioextensions import (
    collect,
    CPU_CORES,
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
    Set,
    Tuple,
)
from utils.ctx import (
    CTX,
)
from utils.logs import (
    log,
)

CHECKS: Tuple[
    Tuple[
        Callable[[SSLContext], Any],
        Dict[
            core_model.FindingEnum,
            Callable[[Any], core_model.Vulnerabilities],
        ],
    ],
    ...,
] = ()


async def analyze_one(
    *,
    index: int,
    ssl_ctx: SSLContext,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    count: int,
) -> None:
    await log("info", "Analyzing ssl %s of %s: %s", index, count, ssl_ctx.info)
    for get_check_ctx, checks in CHECKS:
        for finding, check in checks.items():
            if finding in CTX.config.checks:
                for vulnerability in check(get_check_ctx(ssl_ctx)):
                    await stores[vulnerability.finding].store(vulnerability)


async def get_ssl_contexts() -> Set[SSLContext]:
    return set()


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
            for index, ssl_ctx in enumerate(unique_ssl_contexts)
        ),
        workers=CPU_CORES,
    )
