from aws.iam.structure import (
    is_action_permissive,
    is_public_principal,
    is_resource_permissive,
)
from aws.iam.utils import (
    match_pattern,
)
from aws.model import (
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSS3BucketPolicy,
)
from metaloaders.model import (
    Node,
)
from typing import (
    Iterator,
    Union,
)


def _is_s3_action_writeable(actions: Union[AWSS3BucketPolicy, Node]) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    action_start_with = [
        "Copy",
        "Create",
        "Delete",
        "Put",
        "Restore",
        "Update",
        "Upload",
        "Write",
    ]
    for action in actions_list:
        if any(action.startswith(f"s3:{atw}") for atw in action_start_with):
            return True
    return False


def bucket_policy_allows_public_access_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        effect = stmt_raw.get("Effect", "")
        principal = stmt_raw.get("Principal", "")
        actions = stmt_raw.get("Action", [])
        if (
            effect == "Allow"
            and is_public_principal(principal)
            and _is_s3_action_writeable(actions)
        ):
            if isinstance(stmt, Node):
                yield stmt.inner["Principal"]
            else:
                yield stmt


def match_iam_passrole(action: str) -> bool:
    return match_pattern(action, "iam:PassRole")


def open_passrole_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if stmt_raw["Effect"] == "Allow":
            actions = stmt_raw.get("Action", [])
            resources = stmt_raw.get("Resource", [])
            if isinstance(stmt, Node) and actions and resources:
                actions = stmt.inner.get("Action")
                resources = stmt.inner.get("Resource")
                has_permissive_resources = any(
                    map(is_resource_permissive, resources.raw)
                )
                is_iam_passrole = any(map(match_iam_passrole, actions.raw))

                if has_permissive_resources and is_iam_passrole:
                    yield from (
                        resource
                        for resource in resources.data
                        if is_resource_permissive(resource.raw)
                    )
                    yield from (
                        action
                        for action in actions.data
                        if match_iam_passrole(action.raw)
                    )
            else:
                if all(
                    (
                        any(map(match_iam_passrole, actions)),
                        any(map(is_resource_permissive, resources)),
                    )
                ):
                    yield stmt


def negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data

        if stmt_raw["Effect"] != "Allow":
            continue

        if isinstance(stmt, Node):
            if "NotAction" in stmt_raw:
                yield from (
                    action
                    for action in stmt.inner.get("NotAction").data
                    if not is_action_permissive(action.raw)
                )

            if "NotResource" in stmt_raw:
                yield from (
                    resource
                    for resource in stmt.inner.get("NotResource").data
                    if not is_resource_permissive(resource.raw)
                )
        else:
            if "NotAction" in stmt_raw and not any(
                map(is_action_permissive, stmt_raw["NotAction"])
            ):
                yield stmt

            if "NotResource" in stmt_raw and not any(
                map(is_resource_permissive, stmt_raw["NotResource"])
            ):
                yield stmt


def permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if not (
            stmt_raw["Effect"] == "Allow"
            and "Principal" not in stmt_raw
            and "Condition" not in stmt_raw
        ):
            continue

        actions = stmt_raw.get("Action", [])
        resources = stmt_raw.get("Resource", [])
        has_permissive_resources = any(map(is_resource_permissive, resources))
        has_permissive_actions = any(map(is_action_permissive, actions))
        if (
            isinstance(stmt, Node)
            and has_permissive_resources
            and has_permissive_actions
        ):
            yield from (
                resource
                for resource in stmt.inner.get("Resource").data
                if is_resource_permissive(resource.raw)
            )
            yield from (
                action
                for action in stmt.inner.get("Action").data
                if is_action_permissive(action.raw)
            )

        elif has_permissive_resources and has_permissive_actions:
            yield stmt


def admin_policies_attached_iterate_vulnerabilities(
    managed_policies_iterator: Iterator[Union[Node, AWSIamManagedPolicyArns]],
) -> Iterator[Union[Node, AWSIamManagedPolicyArns]]:
    elevated_policies = {
        "arn:aws:iam::aws:policy/PowerUserAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AdministratorAccess",
    }
    for policies in managed_policies_iterator:
        if isinstance(policies, Node):
            yield from (
                policy
                for policy in policies.data
                if policy.raw in elevated_policies
            )
        elif any(
            policy in elevated_policies for policy in policies.data or []
        ):
            yield policies
