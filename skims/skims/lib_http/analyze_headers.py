from __future__ import (
    annotations,
)

from http_headers import (
    as_string,
    content_security_policy,
    date,
    referrer_policy,
    set_cookie,
    strict_transport_security,
    upgrade_insecure_requests,
    www_authenticate,
    x_content_type_options,
)
from http_headers.types import (
    Header,
)
import inspect
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from multidict import (
    MultiDict,
)
from pathlib import (
    Path,
)
from types import (
    FrameType,
)
from typing import (
    Callable,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
)
from utils.ctx import (
    CTX,
)
from zone import (
    t,
)


class HeaderCheckCtx(NamedTuple):
    headers_parsed: MultiDict[str, Header]
    url_ctx: URLContext


class Location(NamedTuple):
    description: str
    identifier: str


class Locations(NamedTuple):
    locations: List[Location]

    def append(
        self,
        desc: str,
        desc_kwargs: Optional[Dict[str, str]] = None,
        identifier: str = "",
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_http.analyze_headers.{desc}",
                    **(desc_kwargs or {}),
                ),
                identifier=identifier,
            )
        )


def _create_vulns(
    locations: Locations,
    finding: core_model.FindingEnum,
    header: Optional[Header],
    ctx: HeaderCheckCtx,
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
                    value=location.identifier,
                    headers=ctx.url_ctx.headers_raw,
                ),
                source_method=(
                    f"{Path(source.co_filename).stem}.{source.co_name}"
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
        if uri == value:
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


def _content_security_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get("ContentSecurityPolicyHeader"):
        _content_security_policy_block_all_mixed_content(locations, header)
        _content_security_policy_frame_acestors(locations, header)
        _content_security_policy_object_src(locations, header)
        _content_security_policy_script_src(locations, header)
    else:
        locations.append("content_security_policy.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043,
        header=header,
        ctx=ctx,
    )


def _upgrade_insecure_requests(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    head: Optional[Header] = None

    if not ctx.headers_parsed.get("UpgradeInsecureRequestsHeader"):
        if (
            not (head := ctx.headers_parsed.get("ContentSecurityPolicyHeader"))
            or "upgrade-insecure-requests" not in head.directives
        ):
            locations.append("upgrade_insecure_requests.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F043,
        header=head,
        ctx=ctx,
    )


def _date(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get("DateHeader"):
        # Exception: WF(Cannot factorize function)
        if ctx.url_ctx.timestamp_ntp:  # NOSONAR
            minutes: float = (
                abs(ctx.url_ctx.timestamp_ntp - header.date.timestamp()) / 60.0
            )

            if minutes > 1:
                locations.append(
                    desc="date.un_synced",
                    desc_kwargs=dict(
                        minutes=str(int(minutes)),
                        minutes_plural="" if minutes == 1 else "s",
                    ),
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F064,
        header=header,
        ctx=ctx,
    )


def _location(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if response := ctx.url_ctx.custom_f023:
        # Exception: WF(Cannot factorize function)
        if "fluidattacks.com" in response.headers.get(  # NOSONAR
            "location", ""
        ):
            locations.append("location.injection")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F023,
        header=header,
        ctx=ctx,
    )


def _referrer_policy(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    if not ctx.url_ctx.is_html:
        return ()

    locations = Locations(locations=[])
    header: Optional[Header] = None

    if header := ctx.headers_parsed.get("ReferrerPolicyHeader"):
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
        finding=core_model.FindingEnum.F071,
        header=header,
        ctx=ctx,
    )


def _is_sensitive_cookie(cookie_name: str) -> bool:
    sensitive_names = ("session",)
    return any(smell in cookie_name for smell in sensitive_names)


def _set_cookie_httponly(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    headers: List[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if _is_sensitive_cookie(header.cookie_name) and not header.httponly:
            locations.append(
                desc="set_cookie_httponly.missing_httponly",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F128,
        header=None if not headers else headers[0],
        ctx=ctx,
    )


def _set_cookie_samesite(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    headers: List[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if (
            _is_sensitive_cookie(header.cookie_name)
            and header.samesite.lower() != "strict"
        ):
            locations.append(
                desc="set_cookie_samesite.bad_samesite",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F128,
        header=None if not headers else headers[0],
        ctx=ctx,
    )


def _set_cookie_secure(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    headers: List[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if _is_sensitive_cookie(header.cookie_name) and not header.secure:
            locations.append(
                desc="set_cookie_secure.missing_secure",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F130,
        header=None if not headers else headers[0],
        ctx=ctx,
    )


def _strict_transport_security(
    ctx: HeaderCheckCtx,
) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get("StrictTransportSecurityHeader"):
        if val.max_age < 31536000:
            locations.append("strict_transport_security.short_max_age")
    else:
        locations.append("strict_transport_security.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F131,
        header=header,
        ctx=ctx,
    )


def _www_authenticate(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    # FP: analize if the url starts with http
    if not ctx.url_ctx.url.startswith("http://"):  # NOSONAR
        # You can only see plain-text credentials over http
        return ()

    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get("WWWAuthenticate"):
        # Exception: WF(Cannot factorize function)
        if val.type == "basic":  # NOSONAR
            locations.append("www_authenticate.basic")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F015,
        header=header,
        ctx=ctx,
    )


def _x_content_type_options(ctx: HeaderCheckCtx) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])
    header: Optional[Header] = None

    if val := ctx.headers_parsed.get("XContentTypeOptionsHeader"):
        if val.value != "nosniff":
            locations.append("x_content_type_options.insecure")
    else:
        locations.append("x_content_type_options.missing")

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F132,
        header=header,
        ctx=ctx,
    )


def get_check_ctx(url: URLContext) -> HeaderCheckCtx:
    headers_parsed: MultiDict[str, Header] = MultiDict(
        [
            (type(header_parsed).__name__, header_parsed)
            for header_raw_name, header_raw_value in reversed(
                tuple(url.headers_raw.items())
            )
            for line in [f"{header_raw_name}: {header_raw_value}"]
            for header_parsed in [
                content_security_policy.parse(line),
                date.parse(line),
                referrer_policy.parse(line),
                set_cookie.parse(line),
                strict_transport_security.parse(line),
                upgrade_insecure_requests.parse(line),
                www_authenticate.parse(line),
                x_content_type_options.parse(line),
            ]
            if header_parsed is not None
        ]
    )

    return HeaderCheckCtx(
        headers_parsed=headers_parsed,
        url_ctx=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[HeaderCheckCtx], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F015: [_www_authenticate],
    core_model.FindingEnum.F023: [_location],
    core_model.FindingEnum.F128: [_set_cookie_httponly],
    core_model.FindingEnum.F129: [_set_cookie_samesite],
    core_model.FindingEnum.F130: [_set_cookie_secure],
    core_model.FindingEnum.F043: [
        _content_security_policy,
        _upgrade_insecure_requests,
    ],
    core_model.FindingEnum.F071: [_referrer_policy],
    core_model.FindingEnum.F131: [_strict_transport_security],
    core_model.FindingEnum.F132: [_x_content_type_options],
    core_model.FindingEnum.F064: [_date],
}
