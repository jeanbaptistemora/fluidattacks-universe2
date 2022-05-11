from aws.model import (
    AWSDynamoDBTable,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
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
from parse_cfn.structure import (
    iter_dynamodb_table,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_dynamodb_table_unencrypted_iter_vulns(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[Union[AWSDynamoDBTable, Node]]:
    for res in res_iterator:
        if sse_spec := res.inner.get("SSESpecification"):
            enabled = sse_spec.inner.get("SSEEnabled")
            if enabled.raw not in TRUE_OPTIONS:
                yield enabled
        else:
            yield AWSDynamoDBTable(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )


def cfn_dynamodb_table_unencrypted(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f409.cfn_aws_dynamodb_table_unencrypted",
        iterator=get_cloud_iterator(
            _cfn_dynamodb_table_unencrypted_iter_vulns(
                file_ext=file_ext,
                res_iterator=iter_dynamodb_table(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_AWS_DYNAMODB_TABLE_UNENCRYPTED,
    )
