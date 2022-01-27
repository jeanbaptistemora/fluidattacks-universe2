from aws.model import (
    AWSEC2,
    AWSFSxFileSystem,
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
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_ec2_volumes,
    iter_fsx_file_systems,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_fsx_has_unencrypted_volumes_iter_vulns(
    file_ext: str,
    fsx_iterator: Iterator[Union[AWSFSxFileSystem, Node]],
) -> Iterator[Union[AWSFSxFileSystem, Node]]:
    for fsx in fsx_iterator:
        kms_key_id = fsx.inner.get("KmsKeyId")
        if not isinstance(kms_key_id, Node):
            yield AWSFSxFileSystem(
                column=fsx.start_column,
                data=fsx.data,
                line=get_line_by_extension(fsx.start_line, file_ext),
            )


def _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "Encrypted" not in ec2_res.raw:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )
        else:
            vol_encryption = ec2_res.inner.get("Encrypted")
            if vol_encryption.raw in FALSE_OPTIONS:
                yield vol_encryption
            elif "KmsKeyId" not in ec2_res.raw:
                yield AWSEC2(
                    column=ec2_res.start_column,
                    data=ec2_res.data,
                    line=get_line_by_extension(ec2_res.start_line, file_ext),
                )


def cfn_fsx_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F250.value.cwe},
        description_key="src.lib_path.f250.fsx_has_unencrypted_volumes",
        finding=FindingEnum.F250,
        iterator=get_cloud_iterator(
            _cfn_fsx_has_unencrypted_volumes_iter_vulns(
                file_ext=file_ext,
                fsx_iterator=iter_fsx_file_systems(template=template),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )


def cfn_ec2_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F250.value.cwe},
        description_key="src.lib_path.f250.ec2_has_unencrypted_volumes",
        finding=FindingEnum.F250,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_volumes(template=template),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )
