from aws.model import (
    AWSIamPolicyStatement,
    AWSIamRole,
)
from aws.services import (
    ACTIONS_NEW,
)
from contextlib import (
    suppress,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    _yield_statements_from_policy_document_attribute,
    iter_aws_iam_role,
    iter_aws_kms_key_policy_statements,
    iterate_iam_policy_documents,
)
from parse_hcl2.tokens import (
    Attribute,
)
import re
from typing import (
    Any,
    Iterator,
    List,
)


def has_write_actions(actions: Any) -> bool:
    result: bool = False
    for entry in actions if isinstance(actions, list) else [actions]:
        with suppress(ValueError):
            service, action = entry.split(":")
            if service in ACTIONS_NEW:
                if (
                    "*" in action
                    and len(
                        [
                            act
                            for act in ACTIONS_NEW[service].get("write", [])
                            if re.match(action.replace("*", ".*"), act)
                            and act
                            not in ACTIONS_NEW[service].get(
                                "wildcard_resource", []
                            )
                        ]
                    )
                    > 0
                ):
                    result = True
                    break
                if action in ACTIONS_NEW[service].get(
                    "write", []
                ) and action not in ACTIONS_NEW[service].get(
                    "wildcard_resource", []
                ):
                    result = True
                    break
    return result


def has_attribute_wildcard(attribute: Any) -> bool:
    result: bool = False
    for value in attribute if isinstance(attribute, list) else [attribute]:
        if value == "*":
            result = True
            break
    return result


def _tfm_iam_has_wildcard_resource_on_write_action_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in stmts_iterator:
        if _policy_has_excessive_permissions(stmt):
            yield stmt


def _tfm_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in stmts_iterator:
        effect = stmt.data.get("Effect")
        principal = stmt.data.get("Principal")
        p_aws = principal.get("AWS") if principal else None
        if effect == "Allow" and p_aws == "*":
            yield stmt


def _has_admin_access(managed_policies: List[Any]) -> bool:
    if managed_policies:
        for man_pol in managed_policies:
            # IAM role should not have AdministratorAccess policy
            if "AdministratorAccess" in str(man_pol):
                return True
    return False


def _check_assume_role_policies(assume_role_policy: Attribute) -> bool:
    for stmt in _yield_statements_from_policy_document_attribute(
        assume_role_policy
    ):
        effect = stmt.data.get("Effect")
        if effect == "Allow" and stmt.data.get("NotPrincipal"):
            return True
    return False


def _policy_has_excessive_permissions(stmt: AWSIamPolicyStatement) -> bool:
    has_excessive_permissions: bool = False
    effect = stmt.data.get("Effect")
    resources = stmt.data.get("Resource")
    actions = stmt.data.get("Action")

    if effect == "Allow":
        if stmt.data.get("NotAction") or stmt.data.get("NotResource"):
            has_excessive_permissions = True
        if has_attribute_wildcard(resources):
            if has_attribute_wildcard(actions) or has_write_actions(actions):
                has_excessive_permissions = True

    return has_excessive_permissions


def _tfm_iam_role_is_over_privileged_iter_vulns(
    role_iterator: Iterator[AWSIamRole],
) -> Iterator[Any]:
    for res in role_iterator:
        managed_policies = get_attribute(res.data, "managed_policy_arns")
        if managed_policies and _has_admin_access(managed_policies.val):
            yield managed_policies

        assume_role_policy = get_attribute(res.data, "assume_role_policy")
        if assume_role_policy and _check_assume_role_policies(
            assume_role_policy
        ):
            yield assume_role_policy


def tfm_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_has_wildcard_resource_on_write_action"
        ),
        iterator=get_cloud_iterator(
            _tfm_iam_has_wildcard_resource_on_write_action_iter_vulns(
                stmts_iterator=iterate_iam_policy_documents(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_WILDCARD_WRITE,
    )


def tfm_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        iterator=get_cloud_iterator(
            _tfm_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
                stmts_iterator=iter_aws_kms_key_policy_statements(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_KMS_MASTER_KEYS_EXPOSED,
    )


def tfm_iam_role_is_over_privileged(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f325.iam_is_role_over_privileged"),
        iterator=get_cloud_iterator(
            _tfm_iam_role_is_over_privileged_iter_vulns(
                role_iterator=iter_aws_iam_role(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_ROLE_OVER_PRIVILEGED,
    )
