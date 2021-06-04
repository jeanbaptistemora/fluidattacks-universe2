from aioextensions import (
    collect,
    CPU_CORES,
)
from lib_apk.types import (
    APKContext,
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
from utils.function import (
    shield,
)
from utils.logs import (
    log,
)

CHECKS: Tuple[
    Tuple[
        Callable[[APKContext], Any],
        Dict[
            core_model.FindingEnum,
            Callable[[Any], core_model.Vulnerabilities],
        ],
    ],
    ...,
] = ()


@shield(on_error_return=[])
async def analyze_one(
    *,
    apk_ctx: APKContext,
    index: int,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    count: int,
) -> None:
    await log("info", "Analyzing APK %s of %s: %s", index, count, apk_ctx.path)

    for get_check_ctx, checks in CHECKS:
        for finding, check in checks.items():
            if finding in CTX.config.checks:
                for vulnerability in check(get_check_ctx(apk_ctx)):
                    await stores[vulnerability.finding].store(vulnerability)


def get_apk_contexts() -> Set[APKContext]:
    return set(
        APKContext(
            path=path,
        )
        for path in CTX.config.apk.include
    )


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

    unique_apk_contexts: Set[APKContext] = get_apk_contexts()
    count: int = len(unique_apk_contexts)

    await collect(
        (
            analyze_one(
                apk_ctx=apk_ctx,
                index=index,
                stores=stores,
                count=count,
            )
            for index, apk_ctx in enumerate(unique_apk_contexts)
        ),
        workers=CPU_CORES,
    )
