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
from lib_apk.types import (
    APKContext,
)
import lxml.etree  # nosec
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

            analysis = Analysis(vm=None)
            dalviks: List[DalvikVMFormat] = []
            decompiler = DecompilerDAD(dalviks, analysis)
            dalviks.extend(
                DalvikVMFormat(
                    dex,
                    config=None,
                    decompiler=decompiler,
                    using_api=apk_obj.get_target_sdk_version(),
                )
                for dex in apk_obj.get_all_dex()
            )
            for dalvik in dalviks:
                analysis.add(dalvik)
            analysis.create_xref()

        apk_contexts.add(
            APKContext(
                analysis=analysis,
                apk_manifest=apk_manifest,
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

    for index, apk_ctx in enumerate(unique_apk_contexts):
        # Intentional await-inside-for in order to reduce memory consumption
        await analyze_one(
            apk_ctx=apk_ctx,
            index=index,
            stores=stores,
            count=count,
        )
