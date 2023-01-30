from aws.model import (
    AWSCloudfrontDistribution,
)
from lark import (
    Tree,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f016.constants import (
    VULNERABLE_MIN_PROT_VERSIONS,
    VULNERABLE_ORIGIN_SSL_PROTOCOLS,
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
    get_attribute_by_block,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_cloudfront_distribution,
    iter_aws_elb2_listener,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_aws_content_over_insecure_protocols_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if isinstance(resource, AWSCloudfrontDistribution):
            if (
                v_cert := get_argument(
                    key="viewer_certificate",
                    body=resource.data,
                )
            ) and (
                (
                    min_prot := get_block_attribute(
                        v_cert, "minimum_protocol_version"
                    )
                )
                and any(
                    True
                    for protocol in VULNERABLE_MIN_PROT_VERSIONS
                    if protocol == min_prot.val
                )
            ):
                yield min_prot
            if (
                origin := get_argument(
                    key="origin",
                    body=resource.data,
                )
            ) and (
                (
                    ssl_prot := get_attribute_by_block(
                        block=origin,
                        namespace="custom_origin_config",
                        key="origin_ssl_protocols",
                    )
                )
                and not isinstance(ssl_prot.val, Tree)
                and len(
                    set(ssl_prot.val).intersection(
                        VULNERABLE_ORIGIN_SSL_PROTOCOLS
                    )
                )
                > 0
            ):
                yield ssl_prot


def _tfm_aws_elb_without_sslpolicy(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_attribute(resource.data, "ssl_policy"):
            yield resource


def tfm_aws_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        iterator=get_cloud_iterator(
            _tfm_aws_content_over_insecure_protocols_iterate_vulnerabilities(
                resource_iterator=iter_aws_cloudfront_distribution(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_INSEC_PROTO,
    )


def tfm_aws_elb_without_sslpolicy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f016.aws_elb_without_sslpolicy"),
        iterator=get_cloud_iterator(
            _tfm_aws_elb_without_sslpolicy(
                resource_iterator=iter_aws_elb2_listener(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_ELB_WITHOUT_SSLPOLICY,
    )
