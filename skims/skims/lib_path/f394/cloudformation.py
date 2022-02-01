from aws.model import (
    AWSCTrail,
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
    iter_cloudtrail_trail,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_log_files_not_validated_iterate_vulnerabilities(
    file_ext: str,
    trails_iterator: Iterator[Union[AWSCTrail, Node]],
) -> Iterator[Union[AWSCTrail, Node]]:
    values = ["true", "True", True, "1", 1]
    for trail in trails_iterator:
        log_file_val = get_node_by_keys(trail, ["EnableLogFileValidation"])
        if isinstance(log_file_val, Node):
            if log_file_val.raw not in values:
                yield log_file_val
        else:
            yield AWSCTrail(
                data=trail.data,
                column=trail.start_column,
                line=get_line_by_extension(trail.start_line, file_ext),
            )


def cfn_log_files_not_validated(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f394.cfn_log_files_not_validated",
        iterator=get_cloud_iterator(
            _cfn_log_files_not_validated_iterate_vulnerabilities(
                file_ext=file_ext,
                trails_iterator=iter_cloudtrail_trail(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_LOG_NOT_VALIDATED,
    )
