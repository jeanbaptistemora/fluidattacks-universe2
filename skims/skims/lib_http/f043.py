# Standard library
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Type,
)

# Local libraries
from http_headers import (
    as_string,
    content_security_policy,
    referrer_policy,
    strict_transport_security,
    x_content_type_options,
    x_frame_options,
)
from http_headers.types import (
    ContentSecurityPolicyHeader,
    ReferrerPolicyHeader,
    StrictTransportSecurityHeader,
    XContentTypeOptionsHeader,
    XFrameOptionsHeader,
)
from http_headers.types import (
    Header,
)
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)
from zone import (
    t,
)


class HeaderCheckCtx(NamedTuple):
    headers_parsed: Dict[Type[Header], Header]
    headers_raw: Dict[str, str]
    is_html: bool
    url: str


def _create_vulns(
    descriptions: List[str],
    finding: core_model.FindingEnum,
    header: Optional[Header],
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            state=core_model.VulnerabilityStateEnum.OPEN,
            # Must start with home so integrates allows it
            stream="home,response,headers",
            what=serialize_namespace_into_vuln(
                kind=core_model.VulnerabilityKindEnum.INPUTS,
                namespace=CTX.config.namespace,
                what=ctx.url,
            ),
            where=translation,
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=("644",),
                description=translation,
                snippet=as_string.snippet(
                    url=ctx.url,
                    header=header.name if header else None,
                    headers=ctx.headers_raw,
                ),
            ),
        )
        for description in descriptions
        if description
        for description_key, *description_args in [
            description.split("#", maxsplit=1),
        ]
        for translation in [
            t(f"lib_http.f043.{description_key}", *description_args),
        ]
    )


def _content_security_policy_wild_uri(
    descs: List[str],
    value: str,
) -> None:
    for arg in ("data:", "http:", "https:", "://*"):
        if arg in value:
            descs.append(f"content_security_policy.wild_uri#{arg}")


def _content_security_policy_block_all_mixed_content(
    descs: List[str],
    header: Header,
) -> None:
    if "block-all-mixed-content" in header.directives:
        descs.append("content_security_policy.mixed_content_deprecated")


def _content_security_policy_frame_acestors(
    descs: List[str],
    header: Header,
) -> None:
    if values := header.directives.get("frame-ancestors"):
        for value in values:
            _content_security_policy_wild_uri(descs, value)
    else:
        descs.append("content_security_policy.missing_frame_ancestors")


def _content_security_policy_object_src(
    descs: List[str],
    header: Header,
) -> None:
    if (
        "object-src" not in header.directives
        and "default-src" not in header.directives
    ):
        descs.append("content_security_policy.missing_object_src")


def _content_security_policy_script_src(
    descs: List[str],
    header: Header,
) -> None:
    if values := (
        header.directives.get("script-src")
        or header.directives.get("default-src")
    ):
        for value in values:
            if value == "'unsafe-inline'":
                descs.append("content_security_policy.script-src.unsafeinline")

            _content_security_policy_wild_uri(descs, value)

            for arg in (
                "*.amazonaws.com",
                "*.cloudflare.com",
                "*.cloudfront.net",
                "*.doubleclick.net",
                "*.google.com",
                "*.googleapis.com",
                "*.googlesyndication.com",
                "*.newrelic.com",
                "*.s3.amazonaws.com",
                "*.yandex.ru",
                "ajax.googleapis.com",
                "mc.yandex.ru",
                "vk.com",
                "www.google.com",
            ):
                if arg in value:
                    descs.append(
                        f"content_security_policy.script-src.jsonp#{arg}"
                    )
    else:
        descs.append("content_security_policy.missing_script_src")


def _content_security_policy_upgrade_insecure_requests(
    descs: List[str],
    header: Header,
) -> None:
    if "upgrade-insecure-requests" not in header.directives:
        descs.append("content_security_policy.missing_upgrade_insecure")


def _content_security_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    descs: List[str] = []
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get(ContentSecurityPolicyHeader):
        _content_security_policy_block_all_mixed_content(descs, header)
        _content_security_policy_frame_acestors(descs, header)
        _content_security_policy_object_src(descs, header)
        _content_security_policy_script_src(descs, header)
        _content_security_policy_upgrade_insecure_requests(descs, header)
    else:
        descs.append("content_security_policy.missing")

    return _create_vulns(
        descriptions=descs,
        finding=core_model.FindingEnum.F043_DAST_CSP,
        header=header,
        ctx=ctx,
    )


def _referrer_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    desc, header = "", None

    if header := ctx.headers_parsed.get(ReferrerPolicyHeader):
        for value in header.values:
            # Some header values may be out of the spec or experimental
            # We won't take them into account as some browsers won't
            # support them. The spec says that browsers should read the next
            # value in the comma separated list
            if value in {
                "no-referrer",
                "no-referrer-when-downgrade",
                "origin",
                "origin-when-cross-origin",
                "same-origin",
                "strict-origin",
                "strict-origin-when-cross-origin",
                "unsafe-url",
            }:
                desc = (
                    ""
                    if value
                    in {
                        "no-referrer",
                        "same-origin",
                        "strict-origin",
                        "strict-origin-when-cross-origin",
                    }
                    else "referrer_policy.weak"
                )
                break
        else:
            desc = "referrer_policy.weak"

    else:
        desc = "referrer_policy.missing"

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_RP,
        header=header,
        ctx=ctx,
    )


def _strict_transport_security(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    desc, header = "", None

    if val := ctx.headers_parsed.get(StrictTransportSecurityHeader):
        if val.max_age < 31536000:
            desc = "strict_transport_security.short_max_age"
    else:
        desc = "strict_transport_security.missing"

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_STS,
        header=header,
        ctx=ctx,
    )


def _x_content_type_options(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    desc, header = "", None

    if val := ctx.headers_parsed.get(XContentTypeOptionsHeader):
        if val.value != "nosniff":
            desc = "x_content_type_options.insecure"
    else:
        desc = "x_content_type_options.missing"

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_XCTO,
        header=header,
        ctx=ctx,
    )


def _x_frame_options(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    desc, header = "", None

    if val := ctx.headers_parsed.get(XFrameOptionsHeader):
        if val.value not in {"deny", "sameorigin"}:
            desc = "x_frame_options.insecure"
    else:
        desc = "x_frame_options.missing"

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_XFO,
        header=header,
        ctx=ctx,
    )


async def http_headers_configuration(
    url: URLContext,
) -> core_model.Vulnerabilities:
    headers_parsed: Dict[Type[Header], Header] = {
        type(header_parsed): header_parsed
        for header_raw_name, header_raw_value in reversed(
            tuple(
                url.headers_raw.items(),
            )
        )
        for line in [f"{header_raw_name}: {header_raw_value}"]
        for header_parsed in [
            content_security_policy.parse(line),
            referrer_policy.parse(line),
            strict_transport_security.parse(line),
            x_content_type_options.parse(line),
            x_frame_options.parse(line),
        ]
        if header_parsed is not None
    }

    return tuple(
        chain.from_iterable(
            (
                check(
                    HeaderCheckCtx(
                        headers_parsed=headers_parsed,
                        headers_raw=url.headers_raw,
                        is_html=url.is_html,
                        url=url.url,
                    )
                )
                for finding, check in CHECKS.items()
                if finding in CTX.config.checks
            )
        )
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[HeaderCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F043_DAST_CSP: _content_security_policy,
    core_model.FindingEnum.F043_DAST_RP: _referrer_policy,
    core_model.FindingEnum.F043_DAST_STS: _strict_transport_security,
    core_model.FindingEnum.F043_DAST_XCTO: _x_content_type_options,
    core_model.FindingEnum.F043_DAST_XFO: _x_frame_options,
}


def analyze(
    url: URLContext,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = [
        http_headers_configuration(url),
    ]

    return coroutines


def should_run() -> bool:
    return any(finding in CTX.config.checks for finding in CHECKS)
