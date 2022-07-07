from aws.model import (
    AWSIamPolicyAttachment,
    AWSIamPolicyStatement,
    AWSIamRole,
)
from aws.services import (
    ACTIONS,
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
    iter_iam_policy_attachment,
    iter_iam_role_policy_statements,
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
    Pattern,
    Union,
)

WILDCARD_ACTION: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
WILDCARD_RESOURCE: Pattern = re.compile(r"^(\*)$")


def _service_is_present_action(
    actions: Union[str, list], service: str
) -> bool:
    actions = actions if isinstance(actions, list) else [actions]
    for act in actions:
        if act == "*" or act.split(":")[0] == service:
            return True
    return False


def _tfm_iam_has_privileges_over_iam_iter_vulns(
    resource_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in resource_iterator:
        effect = stmt.data.get("Effect", "")
        actions = stmt.data.get("Action", [])
        if effect == "Allow" and _service_is_present_action(actions, "iam"):
            yield stmt


def get_wildcard_nodes(actions: Any, pattern: Pattern) -> bool:
    for act in actions if isinstance(actions, list) else [actions]:
        if pattern.match(act):
            return True
    return False


def _is_statement_miss_configured(stmt: Any) -> bool:
    wildcard_action: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
    effect = stmt.data.get("Effect", "")
    if effect == "Allow" and (
        stmt.data.get("NotAction") or stmt.data.get("NotResource")
    ):
        return True
    if (actions := stmt.data.get("Action", [])) and get_wildcard_nodes(
        actions, wildcard_action
    ):
        return True
    return False


def _tfm_iam_is_policy_miss_configured_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
    policy_iterator: Iterator[AWSIamPolicyAttachment],
) -> Iterator[Union[AWSIamPolicyStatement, Attribute]]:
    for stmt in stmts_iterator:
        if _is_statement_miss_configured(stmt):
            yield stmt
    for pol in policy_iterator:
        if users := get_attribute(pol.data, "Users"):
            yield users


def _policy_actions_has_privilege(
    action: Union[str, List[str]], privilege: str
) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = ACTIONS
    actions = action if isinstance(action, list) else [action]
    for act in actions:
        if act == "*":
            return True
        serv, act_val = act.split(":")
        if act_val.startswith("*"):
            return True
        act_val = (
            act_val[: act_val.index("*")] if act_val.endswith("*") else act_val
        )
        if act_val in write_actions.get(serv, {}).get(privilege, []):
            return True
    return False


def _resource_all(resource: Union[str, List[str]]) -> bool:
    """Check if an action is permitted for any resource."""
    resources = resource if isinstance(resource, list) else [resource]
    for res in resources:
        if res == "*":
            return True
    return False


def _tfm_iam_has_wildcard_resource_on_write_action_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in stmts_iterator:
        effect = stmt.data.get("Effect")
        resource = stmt.data.get("Resource")
        action = stmt.data.get("Action")
        wild_res_node = _resource_all(resource) if resource else None
        if (
            effect
            and effect == "Allow"
            and wild_res_node
            and action
            and _policy_actions_has_privilege(action, "write")
        ):
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
        actions = stmt.data.get("Action")
        effect = stmt.data.get("Effect")

        if effect != "Allow":
            continue
        if stmt.data.get("NotAction") or stmt.data.get("NotPrincipal"):
            return True

        if actions and get_wildcard_nodes(actions, WILDCARD_ACTION):
            return True
    return False


def _check_policy_documents(stmt: AWSIamPolicyStatement) -> bool:
    effect = stmt.data.get("Effect")
    resources = stmt.data.get("Resource")
    actions = stmt.data.get("Action")

    if effect != "Allow":
        return False

    if stmt.data.get("NotAction") or stmt.data.get("NotResource"):
        return True
    if resources and get_wildcard_nodes(resources, WILDCARD_RESOURCE):
        return True
    if actions and get_wildcard_nodes(actions, WILDCARD_ACTION):
        return True
    return False


def _tfm_iam_role_is_over_privileged_iter_vulns(
    role_iterator: Iterator[AWSIamRole],
    role_policy_stmts_iterator: Iterator[AWSIamPolicyStatement],
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
    for stmt in role_policy_stmts_iterator:
        if _check_policy_documents(stmt):
            yield stmt


def tfm_iam_has_privileges_over_iam(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f325.tfm_iam_has_privileges_over_iam",
        iterator=get_cloud_iterator(
            _tfm_iam_has_privileges_over_iam_iter_vulns(
                resource_iterator=iterate_iam_policy_documents(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.EC2_IAM_PRIVILEGES_OVER_IAM,
    )


def tfm_iam_is_policy_miss_configured(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f325.iam_is_policy_miss_configured",
        iterator=get_cloud_iterator(
            _tfm_iam_is_policy_miss_configured_iter_vulns(
                stmts_iterator=iterate_iam_policy_documents(model=model),
                policy_iterator=iter_iam_policy_attachment(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_IAM_POLICY_MISS_CONFIG,
    )


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
                role_policy_stmts_iterator=iter_iam_role_policy_statements(
                    model=model
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_ROLE_OVER_PRIVILEGED,
    )
