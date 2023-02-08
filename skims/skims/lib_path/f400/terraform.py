from aws.model import (
    AWSCTrail,
    AWSLambdaFunction,
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
    iter_aws_cloudtrail,
    iter_aws_elb,
    iter_aws_lambda_function,
)
from parse_hcl2.tokens import (
    Attribute,
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
