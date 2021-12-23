import androguard.core.analysis.analysis
from androguard.core.bytecodes.dvm import (
    ClassDefItem,
    DalvikVMFormat,
)
from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from model import (
    core_model,
)
from operator import (
    attrgetter,
)
from parse_android_manifest import (
    _apk_backups_enabled,
    _apk_debugging_enabled,
    _apk_exported_cp,
    _create_vulns,
    APKCheckCtx,
    Locations,
)
import textwrap
from typing import (
    Callable,
    Dict,
    List,
    Set,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)


def get_activities_source(dvms: list) -> str:
    """Decompile given Dalvik VM images."""
    source = [
        x.get_source()
        for dvm in dvms
        for x in dvm.get_classes()
        if "Activity" in x.name
    ]
    return "".join(source)


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
        finding=core_model.FindingEnum.F103,
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


def _get_method_names(
    analysis: androguard.core.analysis.analysis.Analysis,
) -> List[str]:
    names: List[str] = sorted(
        set(map(attrgetter("name"), analysis.get_methods()))
    )

    return names


def _get_class_names(
    analysis: androguard.core.analysis.analysis.Analysis,
) -> List[str]:
    names: List[str] = sorted(
        set(map(attrgetter("name"), analysis.get_classes()))
    )

    return names


def _no_root_check(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        method_names: List[str] = _get_method_names(ctx.apk_ctx.analysis)

        if not any(
            method_name
            in {
                "checkForBusyBoxBinary",
                "checkForDangerousProps",
                "checkForSuBinary",
                "checkSuExists",
                "isRooted",
                "isRootedExperimentalAsync",
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

    if (
        ctx.apk_ctx.apk_obj is not None
        and ctx.apk_ctx.analysis is not None
        and (
            "Lcom/toyberman/RNSslPinningModule;"
            not in _get_class_names(ctx.apk_ctx.analysis)
        )
    ):
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
        finding=core_model.FindingEnum.F207,
        locations=locations,
    )


def _add_no_obfuscation_location(
    class_name: str,
    class_source: str,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_obfuscation",
        desc_class_name=class_name,
        snippet=make_snippet(
            content=class_source,
            viewport=SnippetViewport(column=0, line=1, wrap=True),
        ),
    )


def _no_obfuscation(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    class_names_unobfuscated: Set[str] = {
        "androidx/annotation/",
        "javax/inject/",
        "androidx/browser/",
        "androidx/viewpager2/",
        "de/greenrobot/",
        "androidx/savedstate/",
        "androidx/media/",
        "butterknife/internal/",
        "androidx/activity/",
        "me/leolin/",
        "androidx/versionedparcelable/",
        "io/nlopez/",
        "butterknife/runtime/",
        "org/unimodules/",
        "androidx/cardview/",
        "com/raizlabs/",
        "androidx/coordinatorlayout/",
        "androidx/viewpager/",
        "androidx/lifecycle/",
        "android/support/",
        "net/openid/",
        "com/amplitude/",
        "androidx/biometric/",
        "com/theartofdev/",
        "androidx/core/",
        "androidx/fragment/",
        "okhttp3/internal/",
        "androidx/recyclerview/",
        "host/exp/",
        "com/bumptech/",
        "androidx/appcompat/",
        "versioned/host/",
        "expo/modules/",
        "com/google/",
        "com/facebook/",
    }

    if ctx.apk_ctx.analysis is not None:
        dvm: DalvikVMFormat
        for dvm in ctx.apk_ctx.analysis.vms:
            class_: ClassDefItem
            for class_ in dvm.get_classes():
                class_name: str = class_.get_name()[1:-1]
                class_is_interface: bool = 0x200 & class_.get_access_flags()
                if not class_is_interface and any(
                    map(class_name.startswith, class_names_unobfuscated)
                ):
                    _add_no_obfuscation_location(
                        class_name=class_name,
                        class_source=class_.get_source(),
                        locations=locations,
                    )
                    break

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F046,
        locations=locations,
    )


def _add_has_fragment_injection_location(
    ctx: APKCheckCtx,
    locations: Locations,
    source: str,
    target_sdk_version: int,
) -> None:
    locations.append(
        desc="has_fragment_injection",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> apk_obj, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the targetSdkVersion attribute
                >>> apk_obj.get_target_sdk_version()
                >>> {repr(target_sdk_version)}
                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ),
    )


def _has_fragment_injection(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None:
        sdk_version = ctx.apk_ctx.apk_obj.get_target_sdk_version()
        target_sdk_version = int(sdk_version) if sdk_version else 0

        act_source = get_activities_source(ctx.apk_ctx.analysis.vms)

        is_vulnerable: bool = (
            target_sdk_version < 19 and "PreferenceActivity" in act_source
        )

        if is_vulnerable:
            _add_has_fragment_injection_location(
                ctx, locations, act_source, target_sdk_version
            )

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F103,
        locations=locations,
    )


def _add_webview_caches_javascript_location(
    ctx: APKCheckCtx,
    locations: Locations,
    source: str,
) -> None:
    locations.append(
        desc="webview_caches_javascript",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.8

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> _, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
        ),
    )


def _webview_caches_javascript(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        act_source = get_activities_source(ctx.apk_ctx.analysis.vms)

        is_vulnerable: bool = (
            "setJavaScriptEnabled" in act_source
            and "clearCache" not in act_source
        )

        if is_vulnerable:
            _add_webview_caches_javascript_location(ctx, locations, act_source)

    return _create_vulns(
        ctx=ctx,
        finding=core_model.FindingEnum.F103,
        locations=locations,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[APKCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F046: _no_obfuscation,
    core_model.FindingEnum.F048: _no_root_check,
    core_model.FindingEnum.F055: _apk_backups_enabled,
    core_model.FindingEnum.F058: _apk_debugging_enabled,
    core_model.FindingEnum.F075: _apk_exported_cp,
    core_model.FindingEnum.F103: _apk_unsigned,
    core_model.FindingEnum.F207: _no_certs_pinning,
}
