from aws.model import (
    AWSInstance,
    AWSLaunchTemplate,
)
from itertools import (
    chain,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_instance,
    iter_aws_launch_template,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "instance_initiated_shutdown_behavior"
                and isinstance(elem.val, str)
                and elem.val.lower() != "terminate"
            ):
                yield elem


def _tfm_ec2_associate_public_ip_address_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if isinstance(resource, AWSLaunchTemplate):
            if network_interfaces := get_argument(
                key="network_interfaces",
                body=resource.data,
            ):
                net_public_ip = get_block_attribute(
                    block=network_interfaces, key="associate_public_ip_address"
                )
                if net_public_ip.val is True:
                    yield net_public_ip
        elif (
            isinstance(resource, AWSInstance)
            and (
                public_ip := get_attribute(
                    body=resource.data, key="associate_public_ip_address"
                )
            )
            and public_ip.val is True
        ):
            yield public_ip


def ec2_has_terminate_shutdown_behavior(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F333.value.cwe},
        description_key="lib_path.f333.ec2_allows_shutdown_command",
        finding=FindingEnum.F333,
        iterator=get_cloud_iterator(
            _ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
                resource_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


def tfm_ec2_associate_public_ip_address(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F333.value.cwe},
        description_key=("lib_path.f333.ec2_public_ip_addresses"),
        finding=FindingEnum.F333,
        iterator=get_cloud_iterator(
            _tfm_ec2_associate_public_ip_address_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_instance(model=model),
                    iter_aws_launch_template(model=model),
                )
            )
        ),
        path=path,
    )
