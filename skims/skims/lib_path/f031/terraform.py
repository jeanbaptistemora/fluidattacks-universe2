from aws.model import (
    AWSIamPolicyStatement,
    AWSIamRole,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    admin_policies_attached_iterate_vulnerabilities,
    bucket_policy_allows_public_access_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
    open_passrole_iterate_vulnerabilities,
    permissive_policy_iterate_vulnerabilities,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
    get_tree_value,
    iterate_resources,
)
from parse_hcl2.structure.aws import (
    iter_aws_iam_role,
    iter_iam_user_policy,
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
import re
from typing import (
    Any,
    Iterator,
    List,
    Union,
)


def _tfm_iam_user_missing_role_based_security_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if attr := get_attribute(resource.data, "name"):
            yield attr


def action_has_full_access_to_ssm(actions: Union[str, List[str]]) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    for action in actions_list:
        if action == "ssm:*":
            return True
    return False


def check_resource_name(
    managed_policies_iterator: Iterator[Any],
    name_resource: str,
) -> bool:
    if any(
        not isinstance(policy.data[0], str)
        and (value := str(get_tree_value(policy.data[0])))
        and value.startswith("aws_iam_role")
        and value.split(".")[1] == name_resource
        for policy in managed_policies_iterator
    ):
        return True
    return False


def check_role_name(
    managed_policies_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
    name_role: str,
) -> bool:
    if any(
        len(attr.namespace) > 1
        and (res_name := attr.namespace[2])
        and check_resource_name(managed_policies_iterator, res_name)
        and (role_name := get_attribute(attr.body, "name"))
        and role_name.val in name_role
        for attr in role_iterator
    ):
        return True
    return False


def action_has_attach_role(
    actions: Union[str, List[str]],
    resources: Union[str, List[str]],
    managed_policies_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    resource_list = resources if isinstance(resources, list) else [resources]
    for action in actions_list:
        if action == "iam:Attach*" and any(
            re.split("::", res)[0].startswith("arn:aws:iam")
            and re.search(r"\$?[A-Za-z0-9_./{}]:role/", res)
            and (
                check_role_name(
                    managed_policies_iterator,
                    role_iterator,
                    re.split(":role/", res)[1],
                )
            )
            for res in resource_list
        ):
            return True
    return False


def _tfm_iam_role_excessive_privilege(
    managed_policies_iterator: Iterator[Any],
    statements_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
) -> Iterator[Any]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        resources = stmt_raw.get("Resource", [])
        actions = stmt_raw.get("Action", [])
        if action_has_attach_role(
            actions, resources, managed_policies_iterator, role_iterator
        ):
            yield stmt


def _tfm_iam_has_full_access_to_ssm_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        effect = stmt_raw.get("Effect", "")
        actions = stmt_raw.get("Action", [])
        if effect == "Allow" and action_has_full_access_to_ssm(actions):
            yield stmt


def _has_admin_access(managed_policies: List[Any]) -> bool:
    if managed_policies:
        for man_pol in managed_policies:
            # IAM role should not have AdministratorAccess policy
            if "AdministratorAccess" in str(man_pol):
                return True
    return False


def _tfm_iam_excessive_privileges_iter_vulns(
    role_iterator: Iterator[AWSIamRole],
) -> Iterator[Any]:
    for res in role_iterator:
        managed_policies = get_attribute(res.data, "managed_policy_arns")
        if managed_policies and _has_admin_access(managed_policies.val):
            yield managed_policies


def terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(
                        model=model,
                        key="policy_arn",
                    )
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ADMIN_POLICY,
    )


def tfm_bucket_policy_allows_public_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        iterator=get_cloud_iterator(
            bucket_policy_allows_public_access_iterate_vulnerabilities(
                statements_iterator=(
                    terraform_iterate_iam_policy_documents(model=model)
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_BUCKET_ALLOWS_PUBLIC,
    )


def tfm_iam_user_missing_role_based_security(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f031.iam_user_missing_role_based_security"
        ),
        iterator=get_cloud_iterator(
            _tfm_iam_user_missing_role_based_security_iterate_vulnerabilities(
                resource_iterator=(iter_iam_user_policy(model=model))
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_MISSING_SECURITY,
    )


def terraform_negative_statement(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.negative_statement",
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_NEGATIVE_STATEMENT,
    )


def terraform_open_passrole(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.open_passrole",
        iterator=get_cloud_iterator(
            open_passrole_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_OPEN_PASSROLE,
    )


def terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_PERMISSIVE_POLICY,
    )


def tfm_iam_has_full_access_to_ssm(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        iterator=get_cloud_iterator(
            _tfm_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_FULL_ACCESS_SSM,
    )


def tfm_iam_excessive_role_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.iam_excessive_role_policy",
        iterator=get_cloud_iterator(
            _tfm_iam_role_excessive_privilege(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(model=model)
                ),
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                ),
                role_iterator=iterate_resources(
                    model, "resource", "aws_iam_role"
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_EXCESSIVE_ROLE_POLICY,
    )


def tfm_iam_excessive_privileges(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f031_aws.permissive_policy"),
        iterator=get_cloud_iterator(
            _tfm_iam_excessive_privileges_iter_vulns(
                role_iterator=iter_aws_iam_role(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ADMIN_MANAGED_POLICIES,
    )
