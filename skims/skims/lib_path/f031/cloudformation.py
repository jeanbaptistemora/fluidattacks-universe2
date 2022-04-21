from aws.model import (
    AWSIamManagedPolicy,
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
from parse_cfn.structure import (
    iter_iam_users,
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
    iterate_managed_policy_arns as cnf_iterate_managed_policy_arns,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_iam_user_missing_role_based_security_iterate_vulnerabilities(
    users_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for user in users_iterator:
        policies_node = user.inner.get("Policies", None)
        if policies_node:
            for policy in policies_node.data:
                yield policy.inner["PolicyName"]


def _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
    iam_iterator: Iterator[Node],
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


def cfn_admin_policy_attached(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=cnf_iterate_managed_policy_arns(
                    template=template,
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ADMIN_POLICY_ATTACHED,
    )


def cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        iterator=get_cloud_iterator(
            bucket_policy_allows_public_access_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_BUCKET_ALLOWS_PUBLIC,
    )


def cfn_iam_user_missing_role_based_security(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f031.iam_user_missing_role_based_security"
        ),
        iterator=get_cloud_iterator(
            _cfn_iam_user_missing_role_based_security_iterate_vulnerabilities(
                users_iterator=iter_iam_users(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_MISSING_SECURITY,
    )


def cfn_negative_statement(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.negative_statement",
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_NEGATIVE_STATEMENT,
    )


def cfn_open_passrole(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.open_passrole",
        iterator=get_cloud_iterator(
            open_passrole_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_OPEN_PASSROLE,
    )


def cfn_permissive_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_PERMISSIVE_POLICY,
    )


def cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        iterator=get_cloud_iterator(
            _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                iam_iterator=cfn_iterate_iam_policy_documents(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_FULL_ACCESS_SSM,
    )
