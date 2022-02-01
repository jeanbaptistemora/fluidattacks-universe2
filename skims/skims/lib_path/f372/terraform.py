from aws.model import (
    AWSCloudfrontDistribution,
)
from itertools import (
    chain,
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
    iterate_block_attributes,
)
from parse_hcl2.structure.aws import (
    iter_aws_cloudfront_distribution,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_app_service,
    iter_azurerm_function_app,
    iter_azurerm_storage_account,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_content_over_http_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if isinstance(resource, AWSCloudfrontDistribution):
            if get_argument(
                key="default_cache_behavior",
                body=resource.data,
            ):
                for attr in iterate_block_attributes(
                    get_argument(
                        body=resource.data, key="default_cache_behavior"
                    )
                ):
                    if (
                        attr.key == "viewer_protocol_policy"
                        and attr.val == "allow-all"
                    ):
                        yield attr
            if get_argument(
                key="ordered_cache_behavior",
                body=resource.data,
            ):
                for attr in iterate_block_attributes(
                    get_argument(
                        body=resource.data, key="ordered_cache_behavior"
                    )
                ):
                    if (
                        attr.key == "viewer_protocol_policy"
                        and attr.val == "allow-all"
                    ):
                        yield attr


def _tfm_azure_kv_only_accessible_over_https_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if https := get_attribute(body=resource.data, key="https_only"):
            if https.val is False:
                yield https
        else:
            yield resource


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


def tfm_azure_kv_only_accessible_over_https(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f372.azure_only_accessible_over_http",
        iterator=get_cloud_iterator(
            _tfm_azure_kv_only_accessible_over_https_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_azurerm_app_service(model=model),
                    iter_azurerm_function_app(model=model),
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_KV_ONLY_ACCESS_HTTPS,
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
