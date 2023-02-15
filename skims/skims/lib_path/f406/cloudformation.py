from aws.model import (
    AWSEFS,
)
from collections.abc import (
    Iterator,
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
    iter_efs_file_systems,
)
from typing import (
    Any,
)


def _cfn_aws_efs_unencrypted_iter_vulns(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[AWSEFS | Node]:
    for res in res_iterator:
        encrypted = res.inner.get("Encrypted")
        if encrypted is None:
            yield AWSEFS(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )
        elif encrypted.raw not in TRUE_OPTIONS:
            yield encrypted


def cfn_aws_efs_unencrypted(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f406.aws_efs_unencrypted",
        iterator=get_cloud_iterator(
            _cfn_aws_efs_unencrypted_iter_vulns(
                file_ext=file_ext,
                res_iterator=iter_efs_file_systems(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_AWS_EFS_UNENCRYPTED,
    )
