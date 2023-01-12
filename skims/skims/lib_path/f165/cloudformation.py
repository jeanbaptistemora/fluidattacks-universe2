from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f165.utils import (
    cfn_iam_permissions_policies_checks,
    iam_trust_policies_checks,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
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


def cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_ROLE_OVER_PRIVILEGED
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f165.iam_is_role_over_privileged"),
        iterator=get_cloud_iterator(
            cfn_iam_permissions_policies_checks(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            ),
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


def cfn_iam_allow_wildcard_action_trust_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_wildcard_action_trust_policy"
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
