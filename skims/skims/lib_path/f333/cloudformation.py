from aws.model import (
    AWSEC2,
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
    iter_ec2_launch_templates,
    iter_ec2_ltemplates_and_instances,
)
from typing import (
    Any,
)


def _cfn_ec2_associate_public_ip_address_iter_vulns(
    ec2_iterator: Iterator[Node],
) -> Iterator[AWSEC2 | Node]:
    for ec2_res in ec2_iterator:
        if hasattr(ec2_res, "raw") and "LaunchTemplateData" in ec2_res.raw:
            ec2_res = ec2_res.inner.get("LaunchTemplateData")
        if not (net_interfaces := ec2_res.inner.get("NetworkInterfaces")):
            continue
        for net_interface in net_interfaces.data:
            if (
                (
                    aso_public_add := net_interface.inner.get(
                        "AssociatePublicIpAddress"
                    )
                )
                and hasattr(aso_public_add, "raw")
                and (
                    not isinstance(aso_public_add.raw, dict)
                    and aso_public_add.raw in TRUE_OPTIONS
                )
            ):
                yield aso_public_add


def _cfn_ec2_has_terminate_shutdown_behavior_iter_vulns(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[AWSEC2 | Node]:
    for ec2_res in ec2_iterator:
        if launch_temp_data := ec2_res.inner.get("LaunchTemplateData"):
            if shut_behavior := launch_temp_data.inner.get(
                "InstanceInitiatedShutdownBehavior"
            ):
                if shut_behavior.raw != "terminate":
                    yield shut_behavior
            else:
                yield AWSEC2(
                    column=launch_temp_data.start_column,
                    data=launch_temp_data.data,
                    line=get_line_by_extension(
                        launch_temp_data.start_line, file_ext
                    ),
                )
        else:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )


def cfn_ec2_associate_public_ip_address(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f333.cfn_ec2_associate_public_ip_address"),
        iterator=get_cloud_iterator(
            _cfn_ec2_associate_public_ip_address_iter_vulns(
                ec2_iterator=iter_ec2_ltemplates_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_ASSOC_PUB_IP,
    )


def cfn_ec2_has_terminate_shutdown_behavior(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f333.cfn_ec2_allows_shutdown_command"),
        iterator=get_cloud_iterator(
            _cfn_ec2_has_terminate_shutdown_behavior_iter_vulns(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_launch_templates(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_TERMINATE_SHUTDOWN_BEHAVIOR,
    )
