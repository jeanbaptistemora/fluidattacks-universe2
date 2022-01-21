from aws.model import (
    AWSCloudfrontDistribution,
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
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute_by_block,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_cloudfront_distribution,
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


def _tfm_aws_content_over_insecure_protocols_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if isinstance(resource, AWSCloudfrontDistribution):
            if v_cert := get_argument(
                key="viewer_certificate",
                body=resource.data,
            ):
                if min_prot := get_block_attribute(
                    v_cert, "minimum_protocol_version"
                ):
                    if any(
                        True
                        for protocol in VULNERABLE_MIN_PROT_VERSIONS
                        if protocol == min_prot.val
                    ):
                        yield min_prot
            if origin := get_argument(
                key="origin",
                body=resource.data,
            ):
                if ssl_prot := get_attribute_by_block(
                    block=origin,
                    namespace="custom_origin_config",
                    key="origin_ssl_protocols",
                ):
                    if (
                        len(
                            set(ssl_prot.val).intersection(
                                VULNERABLE_ORIGIN_SSL_PROTOCOLS
                            )
                        )
                        > 0
                    ):
                        yield ssl_prot


def _tfm_azure_content_over_insecure_protocols_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        protocol_attr = False
        for elem in resource.data:
            if isinstance(elem, Attribute) and elem.key == "min_tls_version":
                protocol_attr = True
                if elem.val in ("TLS1_0", "TLS1_1"):
                    yield elem
        if not protocol_attr:
            yield resource


def tfm_aws_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F016.value.cwe},
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        finding=FindingEnum.F016,
        iterator=get_cloud_iterator(
            _tfm_aws_content_over_insecure_protocols_iterate_vulnerabilities(
                resource_iterator=iter_aws_cloudfront_distribution(model=model)
            )
        ),
        path=path,
    )


def tfm_azure_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F016.value.cwe},
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        finding=FindingEnum.F016,
        iterator=get_cloud_iterator(
            _tfm_azure_content_over_insecure_protocols_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_storage_account(model=model)
            )
        ),
        path=path,
    )
