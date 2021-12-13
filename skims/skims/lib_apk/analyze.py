from androguard.core.analysis.analysis import (
    Analysis,
)
from androguard.core.bytecodes.apk import (
    APK,
)
from androguard.core.bytecodes.dvm import (
    DalvikVMFormat,
)
from androguard.decompiler.decompiler import (
    DecompilerDAD,
)
from bs4 import (
    BeautifulSoup,
)
import contextlib
from lib_apk import (
    analyze_bytecodes,
)
import lxml.etree  # nosec
from model import (
    core_model,
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
    Optional,
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


async def get_apk_context(path: str) -> APKContext:
    apk_obj: Optional[APK] = None
    apk_manifest: Optional[BeautifulSoup] = None
    analysis: Optional[Analysis] = None
    with contextlib.suppress(zipfile.BadZipFile):
        apk_obj = APK(path)

        with contextlib.suppress(KeyError):
            apk_manifest_data = apk_obj.xml["AndroidManifest.xml"]
            apk_manifest = BeautifulSoup(
                BeautifulSoup(
                    lxml.etree.tostring(apk_manifest_data),
                    features="html.parser",
                ).prettify(),
                features="html.parser",
            )

        dalviks = []
        analysis = Analysis()
        for dex in apk_obj.get_all_dex():
            dalvik = DalvikVMFormat(
                dex,
                using_api=apk_obj.get_target_sdk_version(),
            )
            analysis.add(dalvik)
            dalviks.append(dalvik)
            dalvik.set_decompiler(DecompilerDAD(dalviks, analysis))

        analysis.create_xref()

    return APKContext(
        analysis=analysis,
        apk_manifest=apk_manifest,
        apk_obj=apk_obj,
        path=path,
    )


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
