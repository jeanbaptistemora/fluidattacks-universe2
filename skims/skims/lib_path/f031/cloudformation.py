from aws.model import (
    AWSEC2,
    AWSIamManagedPolicy,
    AWSS3BucketPolicy,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    admin_policies_attached_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
    open_passrole_iterate_vulnerabilities,
    permissive_policy_iterate_vulnerabilities,
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
    iter_iam_users,
    iter_s3_bucket_policies,
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
    iterate_managed_policy_arns as cnf_iterate_managed_policy_arns,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _is_s3_action_writeable(actions: Union[AWSS3BucketPolicy, Node]) -> bool:
    action_start_with = [
        "Copy",
        "Create",
        "Delete",
        "Put",
        "Restore",
        "Update",
        "Upload",
        "Write",
    ]
    for action in actions.data:
        if any(
            action.raw.startswith(f"s3:{atw}") for atw in action_start_with
        ):
            return True
    return False


def _cfn_bucket_policy_allows_public_access_iterate_vulnerabilities(
    policies_iterator: Iterator[Union[AWSS3BucketPolicy, Node]],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            principal = statement.raw.get("Principal", "")
            if (
                effect == "Allow"
                and principal == "*"
                and _is_s3_action_writeable(statement.inner["Action"])
            ):
                yield statement.inner["Principal"]


def _cfn_iam_user_missing_role_based_security_iterate_vulnerabilities(
    users_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for user in users_iterator:
        policies_node = user.inner.get("Policies", None)
        if policies_node:
            for policy in policies_node.data:
                yield policy.inner["PolicyName"]


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


#  developer: acuberos@fluidattacks.com
def cfn_admin_policy_attached(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=cnf_iterate_managed_policy_arns(
                    template=template,
                ),
            )
        ),
        path=path,
    )


#  developer: atrujillo@fluidattacks.com
def cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            _cfn_bucket_policy_allows_public_access_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
    )


#  developer: atrujillo@fluidattacks.com
def cfn_iam_user_missing_role_based_security(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key=(
            "src.lib_path.f031.iam_user_missing_role_based_security"
        ),
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            _cfn_iam_user_missing_role_based_security_iterate_vulnerabilities(
                users_iterator=iter_iam_users(template=template),
            )
        ),
        path=path,
    )


#  developer: acuberos@fluidattacks.com
def cfn_negative_statement(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.negative_statement",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


#  developer: acuberos@fluidattacks.com
def cfn_open_passrole(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.open_passrole",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            open_passrole_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


#  developer: acuberos@fluidattacks.com
def cfn_permissive_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


#  developer: atrujillo@fluidattacks.com
def cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key=(
            "src.lib_path.f031.ec2_has_not_an_iam_instance_profile"
        ),
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_instances(template=template),
            )
        ),
        path=path,
    )


#  developer: atrujillo@fluidattacks.com
def cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                iam_iterator=cfn_iterate_iam_policy_documents(
                    template=template
                ),
            )
        ),
        path=path,
    )
