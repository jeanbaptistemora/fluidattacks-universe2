from aws.model import (
    AWSDynamoDBTable,
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
    iter_dynamodb_table,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_has_not_point_in_time_recovery_iterate_vulnerabilities(
    file_ext: str,
    tables_iterator: Iterator[Node],
) -> Iterator[Union[AWSDynamoDBTable, Node]]:
    values = ["false", "False", False, "0", 0]
    for table in tables_iterator:
        pt_recovery = get_node_by_keys(
            table,
            ["PointInTimeRecoverySpecification", "PointInTimeRecoveryEnabled"],
        )
        if isinstance(pt_recovery, Node):
            if pt_recovery.raw in values:
                yield pt_recovery
        else:
            yield AWSDynamoDBTable(
                data=table.data,
                column=table.start_column,
                line=get_line_by_extension(table.start_line, file_ext),
            )


def cfn_has_not_point_in_time_recovery(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f259.has_not_point_in_time_recovery",
        iterator=get_cloud_iterator(
            _cfn_has_not_point_in_time_recovery_iterate_vulnerabilities(
                file_ext=file_ext,
                tables_iterator=iter_dynamodb_table(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_NOT_POINT_TIME_RECOVERY,
    )
