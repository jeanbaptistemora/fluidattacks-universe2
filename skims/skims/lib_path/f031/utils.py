from aws.iam.structure import (
    is_action_permissive,
    is_public_principal,
    is_resource_permissive,
)
from aws.model import (
    AWSIamPolicyStatement,
    AWSS3BucketPolicy,
)
from collections.abc import (
    Iterator,
)
from metaloaders.model import (
    Node,
)


def _is_s3_action_writeable(actions: AWSS3BucketPolicy | Node) -> bool:
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
        if any(
            action.startswith(f"s3:{atw}")  # type: ignore
            for atw in action_start_with
        ):
            return True
    return False


def bucket_policy_allows_public_access_iterate_vulnerabilities(
    statements_iterator: Iterator[AWSIamPolicyStatement | Node],
) -> Iterator[AWSIamPolicyStatement | Node]:
    for stmt in statements_iterator:
        stmt_raw = (
            stmt.raw
            if (isinstance(stmt, Node) and hasattr(stmt, "raw"))
            else stmt.data
        )
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


def get_node_negative_stmt_vulns(
    stmt: Node,
    stmt_raw: Node,
) -> Iterator[AWSIamPolicyStatement | Node]:
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


def negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[AWSIamPolicyStatement | Node],
) -> Iterator[AWSIamPolicyStatement | Node]:
    for stmt in statements_iterator:
        stmt_raw = (
            stmt.raw
            if (isinstance(stmt, Node) and hasattr(stmt, "raw"))
            else stmt.data
        )
        if stmt_raw.get("Effect", "") != "Allow":
            continue

        if isinstance(stmt, Node):
            yield from get_node_negative_stmt_vulns(stmt, stmt_raw)
        else:
            if (
                "NotAction" in stmt_raw
                and not any(map(is_action_permissive, stmt_raw["NotAction"]))
            ) or (
                "NotResource" in stmt_raw
                and not any(
                    map(is_resource_permissive, stmt_raw["NotResource"])
                )
            ):
                yield stmt
