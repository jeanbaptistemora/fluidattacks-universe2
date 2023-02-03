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
    iter_aws_ebs_volume,
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


def _tfm_get_vulns_from_device(
    device: Any,
) -> Iterator[Any]:
    if encrypted_attr := get_block_attribute(block=device, key="encrypted"):
        if encrypted_attr.val is False:
            yield encrypted_attr
    else:
        yield device


def _tfm_ec2_instance_unencrypted_ebs_block_devices_iter_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if root_device := get_argument(
            key="root_block_device",
            body=resource.data,
        ):
            yield from _tfm_get_vulns_from_device(root_device)
        if ebs_device := get_argument(
            key="ebs_block_device",
            body=resource.data,
        ):
            yield from _tfm_get_vulns_from_device(ebs_device)


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


def tfm_ebs_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f250.resource_not_encrypted",
        iterator=get_cloud_iterator(
            _tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
                resource_iterator=iter_aws_ebs_volume(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EBS_UNENCRYPTED_VOLUMES,
    )


def tfm_ec2_instance_unencrypted_ebs_block_devices(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f250.tfm_ec2_instance_unencrypted_ebs_block_devices"
        ),
        iterator=get_cloud_iterator(
            _tfm_ec2_instance_unencrypted_ebs_block_devices_iter_vulns(
                resource_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_UNENCRYPTED_BLOCK_DEVICES,
    )
