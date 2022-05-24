from aws.services import (
    ACTIONS,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
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
)
from parse_hcl2.structure.aws import (
    iter_aws_kms_key_policy_statements,
    iter_iam_policy_attachment,
    iterate_iam_policy_documents,
)
import re
from typing import (
    Any,
    Iterator,
    List,
    Pattern,
    Union,
)


def _service_is_present_action(
    actions: Union[str, list], service: str
) -> bool:
    actions = actions if isinstance(actions, list) else [actions]
    for act in actions:
        if act == "*" or act.split(":")[0] == service:
            return True
    return False


def _tfm_iam_has_privileges_over_iam_iter_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for stmt in resource_iterator:
        effect = stmt.data.get("Effect", "")
        actions = stmt.data.get("Action", [])
        if effect == "Allow" and _service_is_present_action(actions, "iam"):
            yield stmt


def get_wildcard_nodes(actions: Node, pattern: Pattern) -> bool:
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
    stmts_iterator: Iterator[Any], policy_iterator: Iterator[Any]
) -> Iterator[Union[Any, Node]]:
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
    stmts_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
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
    stmts_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for stmt in stmts_iterator:
        effect = stmt.data.get("Effect")
        principal = stmt.data.get("Principal")
        p_aws = principal.get("AWS") if principal else None
        if effect == "Allow" and p_aws == "*":
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
