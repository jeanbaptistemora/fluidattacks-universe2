from aws.model import (
    AWSLambdaFunction,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_lambda_function,
)
from typing import (
    Any,
    Iterator,
)


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
