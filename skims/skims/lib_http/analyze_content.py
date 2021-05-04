# Standard library
from __future__ import (
    annotations,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)

# Third party library
from bs4.element import (
    Tag,
)

# Local libraries
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
from utils.string import (
    to_snippet_blocking,
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
        *desc: str,
        **desc_kwargs: str,
    ) -> Location:
        return Location(
            column=tag.sourcepos,
            description=t(f"lib_http.analyze_content.{desc}", **desc_kwargs),
            line=tag.sourceline,
        )


class ContentCheckCtx(NamedTuple):
    url: URLContext


def build_vulnerabilities(
    locations: List[Location],
    finding: core_model.FindingEnum,
    ctx: ContentCheckCtx,
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            state=core_model.VulnerabilityStateEnum.OPEN,
            # Must start with home so integrates allows it
            stream="home,response,content",
            what=serialize_namespace_into_vuln(
                kind=core_model.VulnerabilityKindEnum.INPUTS,
                namespace=CTX.config.namespace,
                what=ctx.url,
            ),
            where=f"{location.line}",
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(finding.value.cwe,),
                description=location.description,
                snippet=to_snippet_blocking(
                    column=location.column,
                    content=ctx.url.content,
                    line=location.line,
                ),
            ),
        )
        for location in locations
    )


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[ContentCheckCtx], core_model.Vulnerabilities],
] = {}
