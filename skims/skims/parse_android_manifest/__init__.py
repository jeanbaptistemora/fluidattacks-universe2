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
import bs4
from bs4 import (
    BeautifulSoup,
)
import contextlib
import inspect
import lxml.etree  # nosec
from model import (
    core_model,
)
from parse_android_manifest.types import (
    APKContext,
)
from pathlib import (
    Path,
)
from types import (
    FrameType,
)
from typing import (
    cast,
    List,
    NamedTuple,
    Optional,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
import zipfile
from zone import (
    t,
)


class APKCheckCtx(NamedTuple):
    apk_ctx: APKContext


class Location(NamedTuple):
    description: str
    snippet: str


class Locations(NamedTuple):
    locations: List[Location]

    def append(
        self,
        desc: str,
        snippet: str,
        **desc_kwargs: str,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_apk.analyze_bytecodes.{desc}",
                    **desc_kwargs,
                ),
                snippet=snippet,
            )
        )


def _create_vulns(
    ctx: APKCheckCtx,
    finding: core_model.FindingEnum,
    locations: Locations,
) -> core_model.Vulnerabilities:
    source = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            stream="home,apk,bytecodes",
            what=ctx.apk_ctx.path,
            where=location.description,
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(finding.value.cwe,),
                description=location.description,
                snippet=location.snippet,
                source_method=(
                    f"{Path(source.co_filename).stem}.{source.co_name}"
                ),
            ),
        )
        for location in locations.locations
    )


def _add_android_manifest_location(
    *,
    apk_manifest: bs4.BeautifulSoup,
    desc: str,
    locations: Locations,
    tag: bs4.Tag,
    **desc_kwargs: str,
) -> None:
    locations.append(
        desc=desc,
        snippet=make_snippet(
            content=apk_manifest.prettify(),
            viewport=SnippetViewport(
                column=tag.sourcepos,
                line=tag.sourceline,
                wrap=True,
            ),
        ),
        **desc_kwargs,
    )


def _get_caseless_attr(tag: bs4.Tag, key: str, default: str) -> str:
    attr: str
    key = key.lower()
    for attr, value in tag.attrs.items():
        if attr.lower() == key:
            return value
    return default


def _apk_backups_enabled(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_manifest is None:
        return ()

    application: bs4.Tag
    for application in ctx.apk_ctx.apk_manifest.find_all("application"):

        allows_backup: str = _get_caseless_attr(
            application,
            key="android:allowBackup",
            default="not-set",
        ).lower()

        if allows_backup == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="backups_enabled",
                locations=locations,
                tag=application,
            )
        elif allows_backup == "not-set":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="backups_not_configured",
                locations=locations,
                tag=application,
            )

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F055,
        locations=locations,
    )


def _apk_debugging_enabled(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_manifest is None:
        return ()

    application: bs4.Tag
    for application in ctx.apk_ctx.apk_manifest.find_all("application"):

        is_debuggable: str = _get_caseless_attr(
            application,
            key="android:debuggable",
            default="false",
        ).lower()

        if is_debuggable == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="debugging_enabled",
                locations=locations,
                tag=application,
            )

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F058,
        locations=locations,
    )


def _apk_exported_cp(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    if ctx.apk_ctx.apk_manifest is None:
        return ()

    locations: Locations = Locations([])

    provider: bs4.Tag
    for provider in ctx.apk_ctx.apk_manifest.find_all("provider"):
        authority: str = _get_caseless_attr(
            provider,
            key="android:authorities",
            default="",
        ) or _get_caseless_attr(
            provider,
            key="android:name",
            default="",
        )
        exported: str = _get_caseless_attr(
            provider,
            key="android:exported",
            default="false",
        ).lower()
        grant_uri_permissions: str = _get_caseless_attr(
            provider,
            key="android:grantUriPermissions",
            default="false",
        ).lower()

        if exported == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="exported",
                desc_authority=authority,
                locations=locations,
                tag=provider,
            )
        if grant_uri_permissions == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="grants_uri_permissions",
                desc_authority=authority,
                locations=locations,
                tag=provider,
            )

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F075,
        locations=locations,
    )


async def get_apk_context(path: str) -> APKContext:
    apk_obj: Optional[APK] = None
    apk_manifest: Optional[BeautifulSoup] = None
    analysis: Optional[Analysis] = None
    if path.endswith("AndroidManifest.xml"):
        apk_manifest_data = lxml.etree.parse(path)  # nosec

        if apk_manifest_data:
            apk_manifest = BeautifulSoup(
                BeautifulSoup(
                    lxml.etree.tostring(apk_manifest_data),
                    features="html.parser",
                ).prettify(),
                features="html.parser",
            )
    else:
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


def get_check_ctx(apk_ctx: APKContext) -> APKCheckCtx:
    return APKCheckCtx(
        apk_ctx=apk_ctx,
    )
