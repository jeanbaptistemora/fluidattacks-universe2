# Standard library
from __future__ import (
    annotations,
)
from typing import (
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
    date,
    referrer_policy,
    strict_transport_security,
    www_authenticate,
    x_content_type_options,
)
from http_headers.types import (
    ContentSecurityPolicyHeader,
    DateHeader,
    ReferrerPolicyHeader,
    StrictTransportSecurityHeader,
    WWWAuthenticate,
    XContentTypeOptionsHeader,
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
from zone import (
    t,
)


class HeaderCheckCtx(NamedTuple):
    headers_parsed: Dict[Type[Header], Header]
    url_ctx: URLContext


class Location(NamedTuple):
    description: str


class Locations(NamedTuple):
    locations: List[Location]

    def append(
        self,
        desc: str,
        desc_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_http.analyze_headers.{desc}",
                    **(desc_kwargs or {}),
                ),
            )
        )


def _create_vulns(
    locations: Locations,
    finding: core_model.FindingEnum,
    header: Optional[Header],
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            # Must start with home so integrates allows it
            stream="home,response,headers",
            what=ctx.url_ctx.url,
            where=location.description,
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(finding.value.cwe,),
                description=location.description,
                snippet=as_string.snippet(
                    url=ctx.url_ctx.url,
                    header=header.name if header else None,
                    headers=ctx.url_ctx.headers_raw,
                ),
            ),
        )
        for location in locations.locations
    )


def _content_security_policy_wild_uri(
    locations: Locations,
    value: str,
) -> None:
    for uri in ("data:", "http:", "https:", "://*"):
        if uri in value:
            locations.append(
                desc="content_security_policy.wild_uri",
                desc_kwargs=dict(uri=uri),
            )


def _content_security_policy_block_all_mixed_content(
    locations: Locations,
    header: Header,
) -> None:
    if "block-all-mixed-content" in header.directives:
        locations.append("content_security_policy.mixed_content_deprecated")


def _content_security_policy_frame_acestors(
    locations: Locations,
    header: Header,
) -> None:
    if values := header.directives.get("frame-ancestors"):
        for value in values:
            _content_security_policy_wild_uri(locations, value)
    else:
        locations.append("content_security_policy.missing_frame_ancestors")


def _content_security_policy_object_src(
    locations: Locations,
    header: Header,
) -> None:
    if (
        "object-src" not in header.directives
        and "default-src" not in header.directives
    ):
        locations.append("content_security_policy.missing_object_src")


def _content_security_policy_script_src(
    locations: Locations,
    header: Header,
) -> None:
    if values := (
        header.directives.get("script-src")
        or header.directives.get("default-src")
    ):
        for value in values:
            if value == "'unsafe-inline'":
                locations.append(
                    "content_security_policy.script-src.unsafeinline"
                )

            _content_security_policy_wild_uri(locations, value)

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
                    locations.append(
                        desc="content_security_policy.script-src.jsonp",
                        desc_kwargs=dict(host=arg),
                    )
    else:
        locations.append("content_security_policy.missing_script_src")


def _content_security_policy_upgrade_insecure_requests(
    locations: Locations,
    header: Header,
) -> None:
    if "upgrade-insecure-requests" not in header.directives:
        locations.append("content_security_policy.missing_upgrade_insecure")


def _content_security_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get(ContentSecurityPolicyHeader):
        _content_security_policy_block_all_mixed_content(locations, header)
        _content_security_policy_frame_acestors(locations, header)
        _content_security_policy_object_src(locations, header)
        _content_security_policy_script_src(locations, header)
        _content_security_policy_upgrade_insecure_requests(locations, header)
    else:
        locations.append("content_security_policy.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043_DAST_CSP,
        header=header,
        ctx=ctx,
    )


def _date(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get(DateHeader):
        if (
            ctx.url_ctx.timestamp_ntp
            and abs(ctx.url_ctx.timestamp_ntp - header.date.timestamp()) > 60.0
        ):
            locations.append("date.un_synced")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F064_SERVER_CLOCK,
        header=header,
        ctx=ctx,
    )


def _referrer_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

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
                if value not in {
                    "no-referrer",
                    "same-origin",
                    "strict-origin",
                    "strict-origin-when-cross-origin",
                }:
                    locations.append("referrer_policy.weak")
                break
        else:
            locations.append("referrer_policy.weak")

    else:
        locations.append("referrer_policy.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043_DAST_RP,
        header=header,
        ctx=ctx,
    )


def _strict_transport_security(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get(StrictTransportSecurityHeader):
        if val.max_age < 31536000:
            locations.append("strict_transport_security.short_max_age")
    else:
        locations.append("strict_transport_security.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043_DAST_STS,
        header=header,
        ctx=ctx,
    )


def _www_authenticate(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    if not ctx.url_ctx.url.startswith("http://"):
        # You can only see plain-text credentials over http
        return ()

    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get(WWWAuthenticate):
        if val.type == "basic":
            locations.append("www_authenticate.basic")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F015_DAST_BASIC,
        header=header,
        ctx=ctx,
    )


def _x_content_type_options(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get(XContentTypeOptionsHeader):
        if val.value != "nosniff":
            locations.append("x_content_type_options.insecure")
    else:
        locations.append("x_content_type_options.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043_DAST_XCTO,
        header=header,
        ctx=ctx,
    )


def get_check_ctx(url: URLContext) -> HeaderCheckCtx:
    headers_parsed: Dict[Type[Header], Header] = {
        type(header_parsed): header_parsed
        for header_raw_name, header_raw_value in reversed(
            tuple(url.headers_raw.items())
        )
        for line in [f"{header_raw_name}: {header_raw_value}"]
        for header_parsed in [
            content_security_policy.parse(line),
            date.parse(line),
            referrer_policy.parse(line),
            strict_transport_security.parse(line),
            www_authenticate.parse(line),
            x_content_type_options.parse(line),
        ]
        if header_parsed is not None
    }

    return HeaderCheckCtx(
        headers_parsed=headers_parsed,
        url_ctx=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[HeaderCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F015_DAST_BASIC: _www_authenticate,
    core_model.FindingEnum.F043_DAST_CSP: _content_security_policy,
    core_model.FindingEnum.F043_DAST_RP: _referrer_policy,
    core_model.FindingEnum.F043_DAST_STS: _strict_transport_security,
    core_model.FindingEnum.F043_DAST_XCTO: _x_content_type_options,
    core_model.FindingEnum.F064_SERVER_CLOCK: _date,
}
