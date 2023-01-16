from aws.model import (
    AWSIamManagedPolicy,
    AWSKmsKey,
)
from aws.services import (
    ACTIONS,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
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
WILDCARD_RESOURCE: Pattern = re.compile(r"^(\*)$")


def get_wildcard_nodes_for_resources(
    actions: Node, resources: Node, pattern: Pattern
) -> Iterator[Node]:
    exceptions = {
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeInstanceCreditSpecifications",
        "ec2:DescribeInstanceEventNotificationAttributes",
        "ec2:DescribeInstanceEventWindows",
        "ec2:DescribeInstanceTypeOfferings",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeInstances",
        "ec2:DescribeInternetGateways",
        "ec2:DescribeIpamPools",
        "ec2:DescribeIpamScopes",
        "ec2:DescribeIpams",
        "ec2:DescribeIpv6Pools",
        "ec2:DescribeKeyPairs",
    }
    for res in (
        resources.data if isinstance(resources.raw, List) else [resources]
    ):
        is_action_in_exceptions = list(
            map(
                lambda action: str(action.raw) in exceptions,
                actions.data if isinstance(actions.raw, List) else [actions],
            )
        )
        if False in is_action_in_exceptions and pattern.match(res.raw):
            yield res


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


def _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
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


def _policy_actions_has_privilege(action_node: Node, privilege: str) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = ACTIONS
    actions = (
        action_node.data
        if isinstance(action_node.data, list)
        else [action_node]
    )
    for act in actions:
        if act.raw == "*":
            return True
        serv, act_val = act.raw.split(":")
        if act_val.startswith("*"):
            return True
        act_val = (
            act_val[: act_val.index("*")] if act_val.endswith("*") else act_val
        )
        if act_val in write_actions.get(serv, {}).get(privilege, []):
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
    for stm in statements.data:
        effect = get_node_by_keys(stm, ["Effect"])
        resource = get_node_by_keys(stm, ["Resource"])
        action = get_node_by_keys(stm, ["Action"])
        wild_res_node = _resource_all(resource) if resource else None
        if (
            effect
            and effect.raw == "Allow"
            and wild_res_node
            and action
            and _policy_actions_has_privilege(action, "write")
        ):
            yield wild_res_node


def _cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = (
            iam_res.inner["Policies"].data
            if hasattr(iam_res, "raw") and "Policies" in iam_res.raw
            else [iam_res]
        )
        for policy in policies:
            statements = get_node_by_keys(
                policy, ["PolicyDocument", "Statement"]
            )
            if isinstance(statements, Node):
                yield from _policy_statement_privilege(statements)


def _service_is_present_action(
    action_node: Node, service: str
) -> Iterator[Node]:
    actions = (
        action_node.data
        if isinstance(action_node.data, list)
        else [action_node]
    )
    for act in actions:
        if act.raw == "*" or act.raw.split(":")[0] == service:
            yield act


def _iam_is_present_in_action(stmt: Node) -> Iterator[Node]:
    if isinstance(stmt, Node) and hasattr(stmt.inner, "get"):
        effect = stmt.inner.get("Effect")
        if effect.raw == "Allow" and (action := stmt.inner.get("Action")):
            yield from _service_is_present_action(action, "iam")


def _cfn_iam_has_privileges_over_iam_iter_vulns(
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = (
            iam_res.inner["Policies"].data
            if hasattr(iam_res, "raw") and "Policies" in iam_res.raw
            else [iam_res]
        )
        for policy in policies:
            if statements := get_node_by_keys(
                policy, ["PolicyDocument", "Statement"]
            ):
                for stmt in statements.data or []:
                    yield from _iam_is_present_in_action(stmt)


def _is_statement_miss_configured(file_ext: str, stmt: Node) -> Iterator[Node]:
    wildcard_action: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
    effect = stmt.inner.get("Effect")
    if effect.raw == "Allow":
        if no_action := stmt.inner.get("NotAction"):
            yield AWSIamManagedPolicy(
                column=no_action.start_column,
                data=no_action.data,
                line=get_line_by_extension(no_action.start_line, file_ext),
            ) if isinstance(no_action.raw, List) else no_action
        if no_resource := stmt.inner.get("NotResource"):
            yield AWSIamManagedPolicy(
                column=no_resource.start_column,
                data=no_resource.data,
                line=get_line_by_extension(no_resource.start_line, file_ext),
            ) if isinstance(no_resource.raw, List) else no_resource
        action = stmt.inner.get("Action")
        if action:
            yield from get_wildcard_nodes(action, wildcard_action)


def _cfn_iam_is_policy_miss_configured_iter_vulns(
    file_ext: str,
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        pol_document = iam_res.inner.get("PolicyDocument")
        statements = pol_document.inner.get("Statement")
        for stmt in statements.data:
            yield from _is_statement_miss_configured(file_ext, stmt)
        if users := iam_res.inner.get("Users"):
            yield AWSIamManagedPolicy(
                column=users.start_column,
                data=users.data,
                line=get_line_by_extension(users.start_line, file_ext),
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
            _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
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
            _cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_WILDCARD_WRITE,
    )


def cfn_iam_is_policy_miss_configured(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f325.iam_is_policy_miss_configured"),
        iterator=get_cloud_iterator(
            _cfn_iam_is_policy_miss_configured_iter_vulns(
                file_ext=file_ext,
                iam_iterator=iter_iam_managed_policies_and_mgd_policies(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_POLICY_MISS_CONFIG,
    )


def cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f325.iam_has_privileges_over_iam"),
        iterator=get_cloud_iterator(
            _cfn_iam_has_privileges_over_iam_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_PRIVILEGES_OVER_IAM,
    )


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


def cfn_iam_allow_wildcard_action_trust_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_wildcard_action_trust_policy"
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
