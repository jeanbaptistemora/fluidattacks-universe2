from __future__ import (
    annotations,
)

from bs4.element import (
    Tag,
)
import contextlib
import dns
import dns.exception
import dns.resolver
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from model.core_model import (
    LocalesEnum,
    MethodsEnum,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Union,
)
from urllib.parse import (
    urlparse,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
import viewstate
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)
from zone import (
    t,
)


class Location(NamedTuple):
    column: int
    description: str
    line: int

    @classmethod
    def from_soup_tag(
        cls: Any,
        tag: Tag,
        desc: str,
        desc_kwargs: Optional[Dict[str, Union[LocalesEnum, Any]]] = None,
    ) -> Location:
        return Location(
            column=tag.sourcepos,
            description=t(
                f"lib_http.analyze_content.{desc}",
                **(desc_kwargs or {}),
            ),
            line=tag.sourceline,
        )


class ContentCheckCtx(NamedTuple):
    url: URLContext


def build_vulnerabilities(
    locations: List[Location],
    ctx: ContentCheckCtx,
    method: MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=method,
            stream="home,response,content",
            what=ctx.url.url,
            where=str(location.line),
            metadata=build_metadata(
                method=method,
                description=location.description,
                snippet=make_snippet(
                    content=ctx.url.content,
                    viewport=SnippetViewport(
                        column=location.column,
                        line=location.line,
                    ),
                ),
            ),
        )
        for location in locations
    )


def _sub_resource_integrity(
    ctx: ContentCheckCtx,
) -> core_model.Vulnerabilities:
    locations: List[Location] = []

    for script in ctx.url.soup.find_all("script"):
        if not script.get("integrity") and (src := script.get("src")):
            netloc = urlparse(src).netloc

            for domain in (
                "cloudflareinsights.com",
                "cookiebot.com",
                "newrelic.com",
                "nr-data.net",
            ):
                if netloc.endswith(domain):
                    locations.append(
                        Location.from_soup_tag(
                            desc="sub_resource_integrity.missing_integrity",
                            desc_kwargs=dict(netloc=netloc),
                            tag=script,
                        )
                    )

    return build_vulnerabilities(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.SUB_RESOURCE_INTEGRITY,
    )


def _view_state(ctx: ContentCheckCtx) -> core_model.Vulnerabilities:
    locations: List[Location] = []

    for tag in ctx.url.soup.find_all("input"):
        if tag.get("name") == "__VIEWSTATE" and (value := tag.get("value")):
            with contextlib.suppress(viewstate.ViewStateException):
                view_state = viewstate.ViewState(base64=value)
                view_state.decode()

                locations.append(
                    Location.from_soup_tag(
                        desc="view_state.not_encrypted",
                        tag=tag,
                    )
                )

    return build_vulnerabilities(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.VIEW_STATE,
    )


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url=url,
    )


def _query_dns(
    domain: str,
    timeout: float = 2.0,
) -> list:

    resolver = dns.resolver.Resolver()
    record_type = "TXT"
    resource_records = list(
        map(
            lambda r: r.strings,
            resolver.resolve(domain, record_type, lifetime=timeout),
        )
    )
    _resource_record = [
        resource_record[0][:0].join(resource_record)
        for resource_record in resource_records
        if resource_record
    ]
    records = [r.decode() for r in _resource_record]
    return records


def _check_spf_records(ctx: ContentCheckCtx) -> bool:
    domain: str
    validator: bool = False
    txt_records: List[str] = []

    domain = ctx.url.get_base_domain()
    txt_records = _query_dns(domain)
    for record in txt_records:
        if "v=spf1" in record:
            validator = True
    return validator


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[ContentCheckCtx], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F036: [_view_state],
    core_model.FindingEnum.F086: [_sub_resource_integrity],
}
