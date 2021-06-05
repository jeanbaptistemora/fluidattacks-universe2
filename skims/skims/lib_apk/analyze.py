from aioextensions import (
    collect,
    CPU_CORES,
)
import androguard.core.bytecodes.apk
import contextlib
from lib_apk import (
    analyze_bytecodes,
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
    Optional,
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
import zipfile

CHECKS: Tuple[
    Tuple[
        Callable[[APKContext], Any],
        Dict[
            core_model.FindingEnum,
            Callable[[Any], core_model.Vulnerabilities],
        ],
    ],
    ...,
] = ((analyze_bytecodes.get_check_ctx, analyze_bytecodes.CHECKS),)


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
    apk_contexts: Set[APKContext] = set()

    for path in CTX.config.apk.include:

        apk_obj: Optional[androguard.core.bytecodes.apk.APK] = None
        with contextlib.suppress(zipfile.BadZipFile):
            apk_obj = androguard.core.bytecodes.apk.APK(path)

        apk_contexts.add(
            APKContext(
                apk_obj=apk_obj,
                path=path,
            )
        )
    return apk_contexts


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
