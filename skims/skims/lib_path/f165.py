from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    get_vulnerabilities_from_aws_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_cloudfront_distributions,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)


def _has_not_geo_restrictions_iterate_vulnerabilities(
    distributions_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            rest_type = get_node_by_keys(
                dist_config,
                ["Restrictions", "GeoRestriction", "RestrictionType"],
            )
            if isinstance(rest_type, Node) and rest_type.raw == "none":
                yield rest_type


def _cfn_has_not_geo_restrictions(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f165.has_not_geo_restrictions"),
        finding=core_model.FindingEnum.F165,
        path=path,
        statements_iterator=(
            _has_not_geo_restrictions_iterate_vulnerabilities(
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                )
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_has_not_geo_restrictions(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_has_not_geo_restrictions,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_has_not_geo_restrictions(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
