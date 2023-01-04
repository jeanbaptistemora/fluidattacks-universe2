from aws.model import (
    AWSIamManagedPolicy,
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
    iter_iam_roles,
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


def _yield_nodes_from_stmt(stmt: Any, file_ext: str) -> Iterator[Node]:
    if not_actions := stmt.inner.get("NotAction"):
        yield AWSIamManagedPolicy(
            column=not_actions.start_column,
            data=not_actions.data,
            line=get_line_by_extension(not_actions.start_line, file_ext),
        ) if isinstance(not_actions.raw, List) else not_actions

    if not_resource := stmt.inner.get("NotResource"):
        yield AWSIamManagedPolicy(
            column=not_resource.start_column,
            data=not_resource.data,
            line=get_line_by_extension(not_resource.start_line, file_ext),
        ) if isinstance(not_resource.raw, List) else not_resource

    if actions := stmt.inner.get("Action"):
        yield from get_wildcard_nodes(actions, WILDCARD_ACTION)

    if resources := stmt.inner.get("Resource"):
        yield from get_wildcard_nodes_for_resources(
            actions, resources, WILDCARD_RESOURCE
        )


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


def _check_policy_documents(policies: Node, file_ext: str) -> Iterator[Node]:
    for policy in policies.data if policies else []:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for stmt in statements.data if statements else []:
            if (
                hasattr(stmt.inner, "get")
                and (effect := stmt.inner.get("Effect"))
                and effect.raw != "Allow"
            ):
                continue

            yield from _yield_nodes_from_stmt(stmt, file_ext)


def _check_assume_role_policies(
    assume_role_policy: Node, file_ext: str
) -> Iterator[Node]:
    statements = assume_role_policy.inner.get("Statement")
    for stmt in statements.data if statements else []:
        if (
            hasattr(stmt.inner, "get")
            and (effect := stmt.inner.get("Effect"))
            and effect.raw != "Allow"
        ):
            continue

        if not_actions := stmt.inner.get("NotAction"):
            yield AWSIamManagedPolicy(
                column=not_actions.start_column,
                data=not_actions.data,
                line=get_line_by_extension(not_actions.start_line, file_ext),
            ) if isinstance(not_actions.raw, List) else not_actions

        if not_princ := stmt.inner.get("NotPrincipal"):
            yield AWSIamManagedPolicy(  # type: ignore
                column=not_princ.start_column,
                data=not_princ.data,
                line=get_line_by_extension(not_princ.start_line, file_ext),
            )

        if actions := stmt.inner.get("Action"):
            yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def _cfn_iam_is_role_over_privileged_iter_vulns(
    file_ext: str,
    iam_iterator: Iterator[Node],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = iam_res.inner.get("Policies")
        yield from _check_policy_documents(policies, file_ext)

        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            yield from _check_assume_role_policies(
                assume_role_policy, file_ext
            )


def cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f165.iam_is_role_over_privileged"),
        iterator=get_cloud_iterator(
            _cfn_iam_is_role_over_privileged_iter_vulns(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_ROLE_OVER_PRIVILEGED,
    )
