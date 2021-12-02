from __future__ import (
    annotations,
)

from bs4.element import (
    Tag,
)
import contextlib
import inspect
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)
from model.core_model import (
    FindingEnum,
)
from pathlib import (
    Path,
)
from types import (
    FrameType,
)
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
)
from urllib.parse import (
    urlparse,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
import viewstate
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
        desc_kwargs: Optional[Dict[str, str]] = None,
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
    finding: core_model.FindingEnum,
    ctx: ContentCheckCtx,
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
            stream="home,response,content",
            what=ctx.url.url,
            where=f"{location.line}",
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(finding.value.cwe,),
                description=location.description,
                snippet=make_snippet(
                    content=ctx.url.content,
                    viewport=SnippetViewport(
                        column=location.column,
                        line=location.line,
                    ),
                ),
                source_method=(
                    f"{Path(source.co_filename).stem}.{source.co_name}"
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
        finding=FindingEnum.F086,
        locations=locations,
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
        finding=FindingEnum.F036,
        locations=locations,
    )


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[ContentCheckCtx], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F036: [_view_state],
    core_model.FindingEnum.F086: [_sub_resource_integrity],
}
