from aioextensions import (
    in_process,
)
from aws.model import (
    AWSCloudfrontDistribution,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
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
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    get_argument,
    iter_aws_cloudfront_distribution,
    iterate_block_attributes,
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
    TIMEOUT_1MIN,
)


def cfn_content_over_http_iterate_vulnerabilities(
    distributions_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            if "DefaultCacheBehavior" in dist_config.inner:
                def_cache_beh = dist_config.inner["DefaultCacheBehavior"]
                if (
                    isinstance(def_cache_beh, Node)
                    and "ViewerProtocolPolicy" in def_cache_beh.inner
                    and def_cache_beh.raw["ViewerProtocolPolicy"]
                    == "allow-all"
                ):
                    yield def_cache_beh.inner["ViewerProtocolPolicy"]
            if "CacheBehaviors" in dist_config.inner and isinstance(
                dist_config.inner["CacheBehaviors"], Node
            ):
                cache_behaviors = dist_config.inner["CacheBehaviors"]
                for cache_b in cache_behaviors.data:
                    if (
                        "ViewerProtocolPolicy" in cache_b.inner
                        and cache_b.raw["ViewerProtocolPolicy"] == "allow-all"
                    ):
                        yield cache_b.inner["ViewerProtocolPolicy"]


def tfm_content_over_http_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSCloudfrontDistribution, Node]]
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, AWSCloudfrontDistribution):
            if get_argument(
                key="default_cache_behavior",
                body=bucket.data,
            ):
                for attr in iterate_block_attributes(
                    get_argument(
                        body=bucket.data, key="default_cache_behavior"
                    )
                ):
                    if (
                        attr.key == "viewer_protocol_policy"
                        and attr.val == "allow-all"
                    ):
                        yield attr
            if get_argument(
                key="ordered_cache_behavior",
                body=bucket.data,
            ):
                for attr in iterate_block_attributes(
                    get_argument(
                        body=bucket.data, key="ordered_cache_behavior"
                    )
                ):
                    if (
                        attr.key == "viewer_protocol_policy"
                        and attr.val == "allow-all"
                    ):
                        yield attr


def _cfn_serves_content_over_http(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.serves_content_over_http",
        finding=core_model.FindingEnum.F372,
        path=path,
        statements_iterator=cfn_content_over_http_iterate_vulnerabilities(
            distributions_iterator=iter_cloudfront_distributions(
                template=template
            )
        ),
    )


def _tfm_serves_content_over_http(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.serves_content_over_http",
        finding=core_model.FindingEnum.F372,
        path=path,
        statements_iterator=tfm_content_over_http_iterate_vulnerabilities(
            buckets_iterator=iter_aws_cloudfront_distribution(model=model)
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_serves_content_over_http(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_serves_content_over_http,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_serves_content_over_http(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_serves_content_over_http,
        content=content,
        path=path,
        model=model,
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
                cfn_serves_content_over_http(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_serves_content_over_http(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
