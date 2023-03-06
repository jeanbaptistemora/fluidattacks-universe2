from aws.model import (
    AWSEC2,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    FALSE_OPTIONS,
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
    iter_ec2_volumes,
)
from typing import (
    Any,
)


def _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[AWSEC2 | Node]:
    for ec2_res in ec2_iterator:
        if hasattr(ec2_res, "raw") and "Encrypted" not in ec2_res.raw:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )
        else:
            vol_encryption = ec2_res.inner.get("Encrypted")
            if (
                not isinstance(vol_encryption.raw, dict)
                and vol_encryption.raw in FALSE_OPTIONS
            ):
                yield vol_encryption
            elif hasattr(ec2_res, "raw") and "KmsKeyId" not in ec2_res.raw:
                yield AWSEC2(
                    column=ec2_res.start_column,
                    data=ec2_res.data,
                    line=get_line_by_extension(ec2_res.start_line, file_ext),
                )


def cfn_ec2_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f250.ec2_has_unencrypted_volumes",
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_volumes(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_UNENCRYPTED_VOLUMES,
    )
