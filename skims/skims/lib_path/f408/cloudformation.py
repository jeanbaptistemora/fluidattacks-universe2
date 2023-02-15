from aws.model import (
    AWSApiGatewayStage,
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
    iter_api_gateway_stages,
)
from typing import (
    Any,
)


def _cfn_api_gateway_access_logging_disabled_iter_vulns(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[AWSApiGatewayStage]:
    for res in res_iterator:
        access_log = res.inner.get("AccessLogSetting")
        if access_log is None:
            yield AWSApiGatewayStage(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )


def cfn_api_gateway_access_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f408.cfn_has_logging_disabled",
        iterator=get_cloud_iterator(
            _cfn_api_gateway_access_logging_disabled_iter_vulns(
                file_ext=file_ext,
                res_iterator=iter_api_gateway_stages(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_API_GATEWAY_LOGGING_DISABLED,
    )
