from aws.iam.structure import (
    is_action_permissive,
    is_resource_permissive,
)
from aws.model import (
    AWSIamManagedPolicy,
    AWSIamPolicyStatement,
    AWSKmsKey,
)
from aws.services import (
    ACTIONS_NEW,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
)
import re
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Pattern,
    Union,
)
from utils.function import (
    get_node_by_keys,
)

WILDCARD_ACTION: Pattern = re.compile(r"^((\*)|(\w+:\*))$")


def permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = (
            stmt.raw
            if (isinstance(stmt, Node) and hasattr(stmt, "raw"))
            else stmt.data
        )
        if not (
            stmt_raw.get("Effect", "") == "Allow"
            and "Principal" not in stmt_raw
            and "Condition" not in stmt_raw
        ):
            continue

        actions = stmt_raw.get("Action", [])
        resources = stmt_raw.get("Resource", [])
        has_permissive_resources = isinstance(
            resources, (list, tuple)
        ) and any(map(is_resource_permissive, resources))
        has_permissive_actions = any(map(is_action_permissive, actions))
        if (
            isinstance(stmt, Node)
            and has_permissive_resources
            and has_permissive_actions
        ):
            yield from (
                resource
                for resource in stmt.inner.get("Resource").data
                if hasattr(resource, "raw")
                and is_resource_permissive(resource.raw)
            )

        elif has_permissive_resources and has_permissive_actions:
            yield stmt


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


def cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
    keys_iterator: Iterator[Node],
) -> Iterator[Union[AWSKmsKey, Node]]:
    for key in keys_iterator:
        statements = get_node_by_keys(key, ["KeyPolicy", "Statement"])
        if not statements:
            continue
        for stmt in statements.data:
            effect = stmt.raw.get("Effect") if hasattr(stmt, "raw") else ""
            principal = get_node_by_keys(stmt, ["Principal", "AWS"])
            if (
                isinstance(principal, Node)
                and effect == "Allow"
                and principal.raw == "*"
            ):
                yield principal


def _policy_actions_has_privilege(action_node: Node) -> bool:
    """Check if an action have a privilege."""
    actions = (
        action_node.data
        if isinstance(action_node.data, list)
        else [action_node]
    )
    for act in actions:
        serv, act_val = (
            act.raw.split(":")
            if len(act.raw.split(":")) == 2
            else (act.raw.split(":"), "")
        )
        act_value = (
            act_val[: act_val.index("*")] if act_val.endswith("*") else act_val
        )
        if (
            act_value in ACTIONS_NEW[serv].get("write", [])
            or act_val.startswith("*")
        ) and act_value not in ACTIONS_NEW[serv].get("wildcard_resource", []):
            return True
    return False


def _resource_all(resource_node: Node) -> Optional[Node]:
    """Check if an action is permitted for any resource."""
    resources = (
        resource_node.data
        if isinstance(resource_node.data, list)
        else [resource_node]
    )
    for res in resources:
        if hasattr(res, "raw") and res.raw == "*":
            return res
    return None


def _policy_statement_privilege(statements: Node) -> Iterator[Node]:
    """Check if a statement of a policy allow an action in all resources."""
    for stm in statements.data if statements.data else []:
        effect = get_node_by_keys(stm, ["Effect"])
        resource = get_node_by_keys(stm, ["Resource"])
        action = get_node_by_keys(stm, ["Action"])
        wild_res_node = _resource_all(resource) if resource else None
        if (
            effect
            and effect.raw == "Allow"
            and wild_res_node
            and action
            and _policy_actions_has_privilege(action)
        ):
            yield wild_res_node


def cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = (
            iam_res.inner["Policies"].data
            if iam_res.inner.get("Policies")
            else [iam_res]
        )
        for policy in policies if policies else []:
            statements = get_node_by_keys(
                policy, ["PolicyDocument", "Statement"]
            )
            if isinstance(statements, Node):
                yield from _policy_statement_privilege(statements)


def cfn_iam_has_wildcard_resource_on_write_action_trust_policies(
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            statements = (
                assume_role_policy.inner.get("Statement")
                if hasattr(assume_role_policy.inner, "get")
                else None
            )
            yield from _policy_statement_privilege(statements)


def policy_document_actions_wilrcard(stmt: Node) -> Iterator[Node]:
    effect = stmt.inner.get("Effect")
    if effect.raw == "Allow":
        action = stmt.inner.get("Action")
        if action:
            yield from get_wildcard_nodes(action, WILDCARD_ACTION)


def cfn_iam_is_policy_actions_wildcard(
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        if pol_document := iam_res.inner.get("PolicyDocument"):
            statements = pol_document.inner.get("Statement")
            for stmt in statements.data:
                yield from policy_document_actions_wilrcard(stmt)


def _yield_nodes_from_stmt(stmt: Any, method: MethodsEnum) -> Iterator[Node]:
    if method == MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_ACTIONS and (
        actions := stmt.inner.get("Action")
    ):
        yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def _check_policy_documents(
    policies: Node, method: MethodsEnum
) -> Iterator[Node]:
    for policy in policies.data if policies else []:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for stmt in statements.data if statements else []:
            if (
                hasattr(stmt, "inner")
                and hasattr(stmt.inner, "get")
                and (effect := stmt.inner.get("Effect"))
                and effect.raw != "Allow"
            ):
                continue
            yield from _yield_nodes_from_stmt(stmt, method)


def cfn_iam_permissions_policies_checks(
    iam_iterator: Iterator[Node],
    method: MethodsEnum,
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = iam_res.inner.get("Policies")
        yield from _check_policy_documents(policies, method)


def check_assume_role_policies(
    assume_role_policy: Node, method: MethodsEnum
) -> Iterator[Node]:
    statements = (
        assume_role_policy.inner.get("Statement")
        if hasattr(assume_role_policy.inner, "get")
        else None
    )
    for stmt in statements.data if statements else []:
        if (
            hasattr(stmt.inner, "get")
            and (effect := stmt.inner.get("Effect"))
            and effect.raw != "Allow"
        ):
            continue
        if method == MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION and (
            actions := stmt.inner.get("Action")
        ):
            yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def iam_trust_policies_checks(
    iam_iterator: Iterator[Node],
    method: MethodsEnum,
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            yield from check_assume_role_policies(
                assume_role_policy,
                method,
            )
