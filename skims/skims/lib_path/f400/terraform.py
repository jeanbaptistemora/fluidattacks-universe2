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
    iter_aws_api_gateway_stage,
    iter_aws_elb,
    iter_aws_instance,
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_elb_logging_disabled_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        if access_logs := get_argument(body=resource.data, key="access_logs"):
            for elem in iterate_block_attributes(access_logs):
                if elem.key == "enabled" and elem.val is False:
                    yield elem
        else:
            yield resource


def _tfm_s3_buckets_logging_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        logging = get_argument(body=resource.data, key="logging")
        if not logging:
            yield resource


def _tfm_ec2_monitoring_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        monitoring = get_attribute(body=resource.data, key="monitoring")
        if not monitoring:
            yield resource
        elif monitoring.val is False:
            yield monitoring


def _tfm_api_gateway_access_logging_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            body=resource.data,
            key="access_log_settings",
        ):
            yield resource


def tfm_elb_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_logging_disabled",
        iterator=get_cloud_iterator(
            _tfm_elb_logging_disabled_iterate_vulnerabilities(
                resource_iterator=iter_aws_elb(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ELB_LOGGING_DISABLED,
    )


def tfm_s3_buckets_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_logging_disabled",
        iterator=get_cloud_iterator(
            _tfm_s3_buckets_logging_disabled(
                resource_iterator=iter_s3_buckets(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_S3_LOGGING_DISABLED,
    )


def tfm_ec2_monitoring_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_monitoring_disabled",
        iterator=get_cloud_iterator(
            _tfm_ec2_monitoring_disabled(
                resource_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_MONITORING_DISABLED,
    )


def tfm_api_gateway_access_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_logging_disabled",
        iterator=get_cloud_iterator(
            _tfm_api_gateway_access_logging_disabled(
                resource_iterator=iter_aws_api_gateway_stage(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_API_GATEWAY_LOGGING_DISABLED,
    )
