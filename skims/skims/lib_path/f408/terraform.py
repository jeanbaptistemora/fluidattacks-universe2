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
)
from parse_hcl2.structure.aws import (
    iter_aws_api_gateway_stage,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_api_gateway_access_logging_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            body=resource.data,
            key="access_log_settings",
        ):
            yield resource


def tfm_api_gateway_access_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f408.has_logging_disabled",
        iterator=get_cloud_iterator(
            _tfm_api_gateway_access_logging_disabled(
                resource_iterator=iter_aws_api_gateway_stage(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_API_GATEWAY_LOGGING_DISABLED,
    )
