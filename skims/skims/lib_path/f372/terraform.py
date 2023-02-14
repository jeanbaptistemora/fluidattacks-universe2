from aws.model import (
    AWSCloudfrontDistribution,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    iterate_block_attributes,
)
from parse_hcl2.structure.aws import (
    iter_aws_cloudfront_distribution,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_get_vulns_from_block(
    resource: Any,
    key_str: str,
) -> Iterator[Union[Any, Node]]:
    key_cond = "viewer_protocol_policy"
    if get_argument(
        key=key_str,
        body=resource.data,
    ):
        for attr in iterate_block_attributes(
            get_argument(body=resource.data, key=key_str)
        ):
            if attr.key == key_cond and attr.val == "allow-all":
                yield attr


def _tfm_content_over_http_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if isinstance(resource, AWSCloudfrontDistribution):
            yield from _tfm_get_vulns_from_block(
                resource, "default_cache_behavior"
            )
            yield from _tfm_get_vulns_from_block(
                resource, "ordered_cache_behavior"
            )


def tfm_serves_content_over_http(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.serves_content_over_http",
        iterator=get_cloud_iterator(
            _tfm_content_over_http_iterate_vulnerabilities(
                resource_iterator=iter_aws_cloudfront_distribution(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_CONTENT_HTTP,
    )
