# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.model import (
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSLambdaFunction,
    AWSS3Bucket,
    AWSS3LogginConfig,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
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
    iter_aws_cloudtrail,
    iter_aws_elb,
    iter_aws_instance,
    iter_aws_lambda_function,
    iter_s3_buckets,
    iter_s3_logging_configuration,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    List,
    Tuple,
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


def _tfm_get_conditions(
    bucket: AWSS3Bucket,
    logging_iterator: List[AWSS3LogginConfig],
) -> Tuple[bool, bool]:
    has_logging: bool = False
    is_log_bucket: bool = False
    for logging_config in logging_iterator:
        if (
            bucket.name is not None
            and bucket.tf_reference is not None
            and (
                logging_config.target
                in (bucket.name, f"{bucket.tf_reference}.id")
            )
        ):
            is_log_bucket = True
            break
        if (
            bucket.name is not None
            and bucket.tf_reference is not None
            and (
                logging_config.bucket
                in (bucket.name, f"{bucket.tf_reference}.id")
            )
        ):
            has_logging = True
            break
    return (has_logging, is_log_bucket)


def _tfm_s3_buckets_logging_disabled(
    bucket_iterator: Iterator[AWSS3Bucket],
    logging_iterator: Iterator[AWSS3LogginConfig],
) -> Iterator[Any]:
    logging_configs = list(logging_iterator)
    for bucket in bucket_iterator:
        logging = get_argument(body=bucket.data, key="logging")
        if not logging:
            has_logging, is_log_bucket = _tfm_get_conditions(
                bucket, logging_configs
            )
            if not has_logging and not is_log_bucket:
                yield bucket


def _tfm_ec2_monitoring_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        monitoring = get_attribute(body=resource.data, key="monitoring")
        if not monitoring:
            yield resource
        elif monitoring.val is False:
            yield monitoring


def _tfm_distribution_has_logging_disabled_iter_vulns(
    resource_iterator: Iterator[AWSCloudfrontDistribution],
) -> Iterator[AWSCloudfrontDistribution]:
    for resource in resource_iterator:
        log_config = get_argument(resource.data, "logging_config")
        if log_config is None:
            yield resource


def _tfm_trails_not_multiregion_iter_vulns(
    resource_iterator: Iterator[AWSCTrail],
) -> Iterator[Union[Attribute, AWSCTrail]]:
    for resource in resource_iterator:
        multi_reg = get_attribute(resource.data, "is_multi_region_trail")
        if multi_reg is None:
            yield resource
        elif multi_reg.val not in TRUE_OPTIONS:
            yield multi_reg


def _tfm_lambda_tracing_disabled_iter_vulns(
    resource_iterator: Iterator[AWSLambdaFunction],
) -> Iterator[Any]:
    for resource in resource_iterator:
        trace = get_argument(body=resource.data, key="tracing_config")
        if not trace:
            yield resource
        elif (mode := get_block_attribute(trace, "mode")) and (
            mode.val != "Active"
        ):
            yield trace


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
                bucket_iterator=iter_s3_buckets(model=model),
                logging_iterator=iter_s3_logging_configuration(model=model),
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


def tfm_distribution_has_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.tfm_has_logging_config_disabled",
        iterator=get_cloud_iterator(
            _tfm_distribution_has_logging_disabled_iter_vulns(
                resource_iterator=iter_aws_cloudfront_distribution(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_CF_DISTR_LOG_DISABLED,
    )


def tfm_trails_not_multiregion(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.trails_not_multiregion",
        iterator=get_cloud_iterator(
            _tfm_trails_not_multiregion_iter_vulns(
                resource_iterator=iter_aws_cloudtrail(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_TRAILS_NOT_MULTIREGION,
    )


def tfm_lambda_tracing_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.tfm_lambda_func_has_trace_disabled",
        iterator=get_cloud_iterator(
            _tfm_lambda_tracing_disabled_iter_vulns(
                resource_iterator=iter_aws_lambda_function(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_LAMBDA_TRACING_DISABLED,
    )
