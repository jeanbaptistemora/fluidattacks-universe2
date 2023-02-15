from aws.model import (
    AWSElbV2,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_cloudfront_distributions,
    iter_elb2_load_target_groups,
)
from typing import (
    Any,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_get_node_vulnerabilities(
    dist_config: Any,
) -> Iterator[Any | Node]:
    def_cache_beh = (
        dist_config.inner["DefaultCacheBehavior"]
        if "DefaultCacheBehavior" in dist_config.inner
        else None
    )
    if (
        isinstance(def_cache_beh, Node)
        and hasattr(def_cache_beh, "raw")
        and "ViewerProtocolPolicy" in def_cache_beh.inner
        and def_cache_beh.raw["ViewerProtocolPolicy"] == "allow-all"
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


def _cfn_content_over_http_iterate_vulnerabilities(
    distributions_iterator: Iterator[Any | Node],
) -> Iterator[Any | Node]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]  # type: ignore
        if isinstance(dist_config, Node):
            yield from _cfn_get_node_vulnerabilities(dist_config)


def _cfn_elb2_uses_insecure_protocol_iterate_vulnerabilities(
    file_ext: str,
    t_groups_iterator: Iterator[Node],
) -> Iterator[AWSElbV2 | Node]:
    for t_group in t_groups_iterator:
        protocol_node = get_node_by_keys(t_group, ["Protocol"])
        target_type = get_node_by_keys(t_group, ["TargetType"])

        if (protocol_node and protocol_node.data != "HTTP") or (
            target_type and target_type.data == "lambda"
        ):
            continue

        if isinstance(protocol_node, Node):
            yield protocol_node
        else:
            yield AWSElbV2(
                column=t_group.start_column,
                data=t_group.data,
                line=get_line_by_extension(t_group.start_line, file_ext),
            )


def cfn_serves_content_over_http(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.serves_content_over_http",
        iterator=get_cloud_iterator(
            _cfn_content_over_http_iterate_vulnerabilities(
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_CONTENT_HTTP,
    )


def cfn_elb2_uses_insecure_protocol(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.elb2_uses_insecure_protocol",
        iterator=get_cloud_iterator(
            _cfn_elb2_uses_insecure_protocol_iterate_vulnerabilities(
                file_ext=file_ext,
                t_groups_iterator=iter_elb2_load_target_groups(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ELB2_INSEC_PROTO,
    )
