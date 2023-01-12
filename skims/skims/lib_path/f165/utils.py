from aws.model import (
    AWSIamManagedPolicy,
)
from lib_path.common import (
    get_line_by_extension,
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
    Pattern,
    Union,
)
from utils.function import (
    get_node_by_keys,
)

WILDCARD_ACTION: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
WILDCARD_RESOURCE: Pattern = re.compile(r"^(\*)$")


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in (
        act_res.data
        if (hasattr(act_res, "raw") and isinstance(act_res.raw, List))
        else [act_res]
    ):
        if hasattr(act, "raw") and pattern.match(act.raw):
            yield act


def check_type(
    stmt: Any, file_ext: str, method: MethodsEnum
) -> Iterator[Node]:

    if (
        not_actions := stmt.inner.get("NotAction")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_ACTION:
        yield AWSIamManagedPolicy(
            column=not_actions.start_column,
            data=not_actions.data,
            line=get_line_by_extension(not_actions.start_line, file_ext),
        ) if isinstance(not_actions.raw, List) else not_actions

    if (
        not_princ := stmt.inner.get("NotPrincipal")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_PRINCIPAL:
        yield AWSIamManagedPolicy(  # type: ignore
            column=not_princ.start_column,
            data=not_princ.data,
            line=get_line_by_extension(not_princ.start_line, file_ext),
        )

    if (
        actions := stmt.inner.get("Action")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION:
        yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def check_assume_role_policies(
    assume_role_policy: Node, file_ext: str, method: MethodsEnum
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
        yield from check_type(stmt, file_ext, method)


def iam_trust_policies_checks(
    file_ext: str,
    iam_iterator: Iterator[Node],
    method: MethodsEnum,
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            yield from check_assume_role_policies(
                assume_role_policy,
                file_ext,
                method,
            )


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
        resources.data
        if hasattr(resources, "raw") and isinstance(resources.raw, List)
        else [resources]
    ):
        is_action_in_exceptions = list(
            map(
                lambda action: str(action.raw) in exceptions,
                actions.data if isinstance(actions.raw, List) else [actions],
            )
        )
        if (
            hasattr(res, "raw")
            and isinstance(res.raw, str)
            and False in is_action_in_exceptions
            and pattern.match(res.raw)
        ):
            yield res


def _yield_nodes_from_stmt(
    stmt: Any, file_ext: str, method: MethodsEnum
) -> Iterator[Node]:
    if (
        not_actions := stmt.inner.get("NotAction")
    ) and method == MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_ACTION:
        yield AWSIamManagedPolicy(
            column=not_actions.start_column,
            data=not_actions.data,
            line=get_line_by_extension(not_actions.start_line, file_ext),
        ) if isinstance(not_actions.raw, List) else not_actions

    if (
        not_resource := stmt.inner.get("NotResource")
    ) and method == MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_RESOURCE:
        yield AWSIamManagedPolicy(
            column=not_resource.start_column,
            data=not_resource.data,
            line=get_line_by_extension(not_resource.start_line, file_ext),
        ) if isinstance(not_resource.raw, List) else not_resource

    if (
        actions := stmt.inner.get("Action")
    ) and method == MethodsEnum.CFN_IAM_ROLE_OVER_PRIVILEGED:
        yield from get_wildcard_nodes(actions, WILDCARD_ACTION)

    if (
        resources := stmt.inner.get("Resource")
    ) and method == MethodsEnum.CFN_IAM_ROLE_OVER_PRIVILEGED:
        yield from get_wildcard_nodes_for_resources(
            actions, resources, WILDCARD_RESOURCE
        )


def _check_policy_documents(
    policies: Node, file_ext: str, method: MethodsEnum
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
            yield from _yield_nodes_from_stmt(stmt, file_ext, method)


def cfn_iam_permissions_policies_checks(
    file_ext: str,
    iam_iterator: Iterator[Node],
    method: MethodsEnum,
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = iam_res.inner.get("Policies")
        yield from _check_policy_documents(policies, file_ext, method)
