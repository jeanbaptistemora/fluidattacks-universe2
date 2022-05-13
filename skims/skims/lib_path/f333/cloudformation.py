from aws.model import (
    AWSEC2,
)
from lib_path.common import (
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
    iter_ec2_instances,
    iter_ec2_launch_templates,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "IamInstanceProfile" not in ec2_res.inner:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )


def _cfn_ec2_has_terminate_shutdown_behavior_iter_vulns(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[Union[AWSEC2, Node]]:
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


def cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f333.ec2_has_not_an_iam_instance_profile"
        ),
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_instances(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_NO_IAM,
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
