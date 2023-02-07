from aws.model import (
    AWSCloudfrontDistribution,
    AWSLbTargetGroup,
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
    get_attribute,
    get_block_attribute,
    iterate_block_attributes,
)
from parse_hcl2.structure.aws import (
    iter_aws_cloudfront_distribution,
    iter_aws_lb_target_group,
    iter_aws_security_group,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_storage_account,
)
from parse_hcl2.tokens import (
    Attribute,
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


def _tfm_elb2_uses_insecure_protocol_iterate_vulnerabilities(
    resource_iterator: Iterator[AWSLbTargetGroup],
) -> Iterator[Union[Attribute, AWSLbTargetGroup]]:
    for res in resource_iterator:
        unsafe_protos = ("HTTP",)
        protocol = get_attribute(res.data, "protocol")
        target_type = get_attribute(res.data, "target_type")
        is_proto_required = (
            target_type.val != "lambda" if target_type else False
        )
        if not is_proto_required:
            continue
        if protocol is None:
            yield res
        elif protocol.val in unsafe_protos:
            yield protocol


def _tfm_azure_sa_insecure_transfer_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if (
            https := get_attribute(
                body=resource.data, key="enable_https_traffic_only"
            )
        ) and https.val is False:
            yield https


def _tfm_aws_sec_group_using_http(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:

    for resource in resource_iterator:
        if ingress_block := get_argument(
            key="ingress",
            body=resource.data,
        ):
            protocol = get_block_attribute(block=ingress_block, key="protocol")
            from_port = get_block_attribute(
                block=ingress_block, key="from_port"
            )
            if (
                protocol
                and protocol.val in {6, "tcp"}
                and from_port
                and from_port.val == 80
            ):
                yield protocol


def tfm_elb2_uses_insecure_protocol(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f372.elb2_uses_insecure_protocol",
        iterator=get_cloud_iterator(
            _tfm_elb2_uses_insecure_protocol_iterate_vulnerabilities(
                resource_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ELB2_INSEC_PROTO,
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


def tfm_azure_sa_insecure_transfer(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f372.tfm_azure_storage_account_insecure_transfer"
        ),
        iterator=get_cloud_iterator(
            _tfm_azure_sa_insecure_transfer_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_storage_account(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_SA_INSEC_TRANSFER,
    )


def tfm_aws_sec_group_using_http(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f372.tfm_aws_sec_group_using_http"),
        iterator=get_cloud_iterator(
            _tfm_aws_sec_group_using_http(
                resource_iterator=iter_aws_security_group(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_SEC_GROUP_USING_HTTP,
    )
