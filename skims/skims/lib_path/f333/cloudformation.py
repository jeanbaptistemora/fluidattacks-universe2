from aws.model import (
    AWSEC2,
    AWSIamManagedPolicy,
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
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_ec2_instances,
    iterate_iam_policy_documents,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "IamInstanceProfile" not in ec2_res.inner:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )


def _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for stmt in iam_iterator:
        effect = stmt.inner.get("Effect")
        action = stmt.inner.get("Action")
        if effect and action and effect.raw == "Allow":
            if isinstance(action.raw, list):
                for act in action.data:
                    if act.raw == "ssm:*":
                        yield act
            else:
                if action.raw == "ssm:*":
                    yield action


def cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F333.value.cwe},
        description_key=(
            "src.lib_path.f333.ec2_has_not_an_iam_instance_profile"
        ),
        finding=FindingEnum.F333,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_instances(template=template),
            )
        ),
        path=path,
    )


def cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F333.value.cwe},
        description_key="src.lib_path.f333.iam_has_full_access_to_ssm",
        finding=FindingEnum.F333,
        iterator=get_cloud_iterator(
            _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                iam_iterator=iterate_iam_policy_documents(template=template),
            )
        ),
        path=path,
    )
