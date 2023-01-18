from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f165.utils import (
    cfn_iam_is_policy_applying_to_users_check,
    cfn_iam_permissions_policies_checks,
    iam_trust_policies_checks,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_iam_managed_policies_and_mgd_policies,
    iter_iam_roles,
)
from typing import (
    Any,
)


def cfn_iam_allow_not_resource_perms_policies(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_RESOURCE
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_not_resourse_permissions_policy"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_permissions_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_allow_not_action_perms_policies(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_ACTION
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_not_action_permissions_policy"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_permissions_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_wildcard_resources_perms_policies(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_RESOURCES
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_wildcard_resources_permissions_policy"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_permissions_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_allow_not_principal_trust_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_PRINCIPAL
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_not_principal_trust_policy"
        ),
        iterator=get_cloud_iterator(
            iam_trust_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_allow_not_actions_trust_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_ACTION
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_not_action_trust_policy"
        ),
        iterator=get_cloud_iterator(
            iam_trust_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_is_policy_applying_to_users(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f165.iam_policies_applying_to_users"),
        iterator=get_cloud_iterator(
            cfn_iam_is_policy_applying_to_users_check(
                file_ext=file_ext,
                iam_iterator=iter_iam_managed_policies_and_mgd_policies(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_APLLY_USERS,
    )
