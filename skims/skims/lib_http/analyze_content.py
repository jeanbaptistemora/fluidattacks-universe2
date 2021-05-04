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
from urllib.parse import (
    urlparse,
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
from model.core_model import (
    FindingEnum,
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
        desc: str,
        desc_kwargs: Dict[str, str],
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


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[ContentCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F086: _sub_resource_integrity,
}
