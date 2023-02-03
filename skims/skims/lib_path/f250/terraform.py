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
    iter_aws_instance,
)
from typing import (
    Any,
    Iterator,
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
