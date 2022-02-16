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
    iter_aws_dynambodb_table,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_aws_dynamodb_table_unencrypted(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if root_block := get_argument(
            body=resource.data,
            key="server_side_encryption",
        ):
            encrypted = get_block_attribute(block=root_block, key="enabled")
            if not encrypted:
                yield root_block
            if encrypted.val is False:
                yield encrypted
        else:
            yield resource


def tfm_aws_dynamodb_table_unencrypted(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f409.tfm_aws_dynamodb_table_unencrypted",
        iterator=get_cloud_iterator(
            _tfm_aws_dynamodb_table_unencrypted(
                resource_iterator=iter_aws_dynambodb_table(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_DYNAMODB_TABLE_UNENCRYPTED,
    )
