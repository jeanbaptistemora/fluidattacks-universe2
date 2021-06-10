from lib_apk.types import (
    APKContext,
)
from model import (
    core_model,
)
from operator import (
    attrgetter,
)
import textwrap
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
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
            ),
        )
        for location in locations.locations
    )


def _add_apk_unsigned_not_signed_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="apk_unsigned",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8
                >>> from androguard.core.bytecodes.apk import APK  # 3.3.5
                >>> apk = APK({repr(ctx.apk_ctx.path)})
                >>> apk.get_signature_names()
                []  # Empty list
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=4, wrap=True),
        ),
    )


def _apk_unsigned(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None:
        signatures: List[str] = ctx.apk_ctx.apk_obj.get_signature_names()

        if not signatures:
            _add_apk_unsigned_not_signed_location(ctx, locations)

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F103_APK_UNSIGNED,
        locations=locations,
    )


def _add_no_root_check_location(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: List[str],
) -> None:
    locations.append(
        desc="no_root_check",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8
                >>> from androguard.misc import AnalyzeAPK  # 3.3.5
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=4, wrap=True),
        ),
    )


def _no_root_check(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        method_names: List[str] = sorted(
            set(map(attrgetter("name"), ctx.apk_ctx.analysis.get_methods()))
        )

        if not any(
            method_name
            in {
                "checkForBusyBoxBinary",
                "checkForDangerousProps",
                "checkForSuBinary",
                "checkSuExists",
                "isRooted",
            }
            for method_name in method_names
        ):
            _add_no_root_check_location(ctx, locations, method_names)

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F048,
        locations=locations,
    )


def get_check_ctx(apk_ctx: APKContext) -> APKCheckCtx:
    return APKCheckCtx(
        apk_ctx=apk_ctx,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[APKCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F048: _no_root_check,
    core_model.FindingEnum.F103_APK_UNSIGNED: _apk_unsigned,
}
