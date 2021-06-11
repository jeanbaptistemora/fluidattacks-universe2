from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
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

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Check the META-INF/ folder and retrieve signature pairs
                >>> # with extensions: .DSA & .DF, .EC & .DF, or .RSA & .DF
                >>> apk.get_signature_names()
                []  # Empty list means no signatures exist
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
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

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse all Dalvik Executables (classes*.dex) in the APK
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
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


def _add_no_certs_pinning_1_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_certs_pinning_config",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # List all files in the APK
                >>> apk_files = apk.zip.nameslist()
                >>> "res/xml/network_security_config.xml" in apk_files
                False  # No network security config exists
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=11, wrap=True),
        ),
    )


def _add_no_certs_pinning_2_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_certs_pinning",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK
                >>> # and version 4.9.3 of "beautifulsoup4"
                >>> from bs4 import BeautifulSoup

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Read and parse the Network Security Config manifest
                >>> nsc = apk.get_file("res/xml/network_security_config.xml")
                >>> BeautifulSoup(nsc).find_all("pin-set")
                []  # Empty list means no <pin-set> tags were defined
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=13, wrap=True),
        ),
    )


def _no_certs_pinning(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None:
        try:
            nsc: str = "res/xml/network_security_config.xml"
            nsc_content: bytes = ctx.apk_ctx.apk_obj.zip.read(nsc)
        except KeyError:
            # No network security config exists
            _add_no_certs_pinning_1_location(ctx, locations)
        else:
            nsc_parsed: Tag = BeautifulSoup(nsc_content, features="xml")
            if not list(nsc_parsed.find_all("pin-set")):
                # No pin sets exist
                _add_no_certs_pinning_2_location(ctx, locations)

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F049_APK_PIN,
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
    core_model.FindingEnum.F049_APK_PIN: _no_certs_pinning,
    core_model.FindingEnum.F103_APK_UNSIGNED: _apk_unsigned,
}
