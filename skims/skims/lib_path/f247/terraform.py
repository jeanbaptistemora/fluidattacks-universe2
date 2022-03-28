from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
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
    iter_aws_ebs_encryption_by_default,
    iter_aws_ebs_volume,
    iter_aws_fsx_windows_file_system,
    iter_aws_instance,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_ebs_unencrypted_by_default_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "enabled"
                and elem.val is False
            ):
                yield elem


def _tfm_ec2_unencrypted_volumes_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if root_device := get_argument(
            key="root_block_device",
            body=resource.data,
        ):
            if root_encrypted_attr := get_block_attribute(
                block=root_device, key="encrypted"
            ):
                if root_encrypted_attr.val is False:
                    yield root_encrypted_attr
            else:
                yield root_device
        if ebs_device := get_argument(
            key="ebs_block_device",
            body=resource.data,
        ):
            if ebs_encrypted_attr := get_block_attribute(
                block=ebs_device, key="encrypted"
            ):
                if ebs_encrypted_attr.val is False:
                    yield ebs_encrypted_attr
            else:
                yield ebs_device


def _tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        encrypted_attr = False
        for elem in resource.data:
            if isinstance(elem, Attribute) and elem.key == "encrypted":
                encrypted_attr = True
                if elem.val is False:
                    yield elem
        if not encrypted_attr:
            yield resource


def _tfm_fsx_unencrypted_volumes_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        kms_key = False
        for elem in resource.data:
            if isinstance(elem, Attribute) and elem.key == "kms_key_id":
                kms_key = True
        if not kms_key:
            yield resource


def tfm_fsx_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f247.tfm_fsx_unencrypted_volumes",
        iterator=get_cloud_iterator(
            _tfm_fsx_unencrypted_volumes_iterate_vulnerabilities(
                resource_iterator=iter_aws_fsx_windows_file_system(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_FSX_UNENCRYPTED_VOLUMES,
    )


def tfm_ebs_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f247.resource_not_encrypted",
        iterator=get_cloud_iterator(
            _tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
                resource_iterator=iter_aws_ebs_volume(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EBS_UNENCRYPTED_VOLUMES,
    )


def tfm_ec2_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f247.resource_not_encrypted",
        iterator=get_cloud_iterator(
            _tfm_ec2_unencrypted_volumes_iterate_vulnerabilities(
                resource_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_UNENCRYPTED_VOLUMES,
    )


def tfm_ebs_unencrypted_by_default(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f247.tfm_ebs_unencrypted_by_default",
        iterator=get_cloud_iterator(
            _tfm_ebs_unencrypted_by_default_iterate_vulnerabilities(
                resource_iterator=iter_aws_ebs_encryption_by_default(
                    model=model
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EBS_UNENCRYPTED_DEFAULT,
    )
