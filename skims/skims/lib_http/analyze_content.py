from __future__ import (
    annotations,
)

from bs4.element import (
    Tag,
)
from collections.abc import (
    Callable,
    Iterable,
)
import contextlib
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from model.core_model import (
    HTTPProperties,
    LocalesEnum,
    MethodsEnum,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
    NamedTuple,
)
from urllib.parse import (
    urlparse,
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
        desc_kwargs: dict[str, LocalesEnum | Any] | None = None,
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
    locations: Iterable[Location],
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
                ).content,
                http_properties=HTTPProperties(
                    has_redirect=ctx.url.has_redirect,
                    original_url=ctx.url.original_url,
                ),
            ),
        )
        for location in locations
    )


def _sub_resource_integrity(
    ctx: ContentCheckCtx,
) -> core_model.Vulnerabilities:
    locations: list[Location] = []

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
    locations: list[Location] = []

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


CHECKS: dict[
    core_model.FindingEnum,
    list[Callable[[ContentCheckCtx], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F036: [_view_state],
    core_model.FindingEnum.F086: [_sub_resource_integrity],
}
