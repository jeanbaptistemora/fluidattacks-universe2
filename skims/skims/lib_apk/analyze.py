from lib_apk import (
    analyze_bytecodes,
)
from model import (
    core_model,
)
from parse_android_manifest import (
    get_apk_context,
)
from parse_android_manifest.types import (
    APKContext,
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
from utils.fs import (
    resolve_paths,
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


async def get_apk_contexts() -> Set[APKContext]:
    apk_contexts: Set[APKContext] = set()

    unique_paths, unique_nu_paths, unique_nv_paths = await resolve_paths(
        exclude=CTX.config.apk.exclude,
        include=CTX.config.apk.include,
    )

    for path in unique_paths | unique_nu_paths | unique_nv_paths:

        apk_contexts.add(await get_apk_context(path))

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

    unique_apk_contexts: Set[APKContext] = await get_apk_contexts()
    count: int = len(unique_apk_contexts)

    for index, apk_ctx in enumerate(unique_apk_contexts):
        # Intentional await-inside-for in order to reduce memory consumption
        await analyze_one(
            apk_ctx=apk_ctx,
            index=index,
            stores=stores,
            count=count,
        )
