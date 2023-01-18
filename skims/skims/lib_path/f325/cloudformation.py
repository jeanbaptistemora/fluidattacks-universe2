from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f325.utils import (
    cfn_iam_has_privileges_over_iam_iter_vulns,
    cfn_iam_has_wildcard_resource_on_write_action_iter_vulns,
    cfn_iam_is_policy_actions_wildcard,
    cfn_iam_permissions_policies_checks,
    cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns,
    iam_trust_policies_checks,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_iam_managed_policies_and_mgd_policies,
    iter_iam_managed_policies_and_roles,
    iter_iam_roles,
    iter_kms_keys,
)
from typing import (
    Any,
)


def cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        iterator=get_cloud_iterator(
            cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_KMS_MASTER_KEYS_EXPOSED,
    )


def cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_has_wildcard_resource_on_write_action"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_WILDCARD_WRITE,
    )


def cfn_iam_is_policy_actions_wildcards(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_allow_wilcard_actions_permissions_policy"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_is_policy_actions_wildcard(
                iam_iterator=iter_iam_managed_policies_and_mgd_policies(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_ACTIONS,
    )


def cfn_iam_allow_wildcard_actions_perms_policies(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_ACTIONS
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_allow_wilcard_actions_permissions_policy"
        ),
        iterator=get_cloud_iterator(
            cfn_iam_permissions_policies_checks(
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )


def cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f325.iam_has_privileges_over_iam"),
        iterator=get_cloud_iterator(
            cfn_iam_has_privileges_over_iam_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_PRIVILEGES_OVER_IAM,
    )


def cfn_iam_allow_wildcard_action_trust_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_allow_wildcard_action_trust_policy"
        ),
        iterator=get_cloud_iterator(
            iam_trust_policies_checks(
                iam_iterator=iter_iam_roles(template=template),
                method=method,
            )
        ),
        path=path,
        method=method,
    )
