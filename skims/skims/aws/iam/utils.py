from collections import (
    UserList,
)
from collections.abc import (
    Iterator,
)
from metaloaders.model import (
    Node,
    Type,
)
import re
from typing import (
    Any,
)


def match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r".*".join(map(re.escape, pattern.split("*")))

    return bool(re.match(f"^{pattern}$", target, flags=flags))


def patch_statement_node(stmt: Node) -> Node:
    stmt.inner.setdefault("Effect", "Deny")
    allow_keys = {"Action", "NotAction", "NotResource", "Resource"}
    keys_to_change = []
    for key, value in stmt.data.items() if hasattr(stmt, "data") else []:
        if (key.inner in allow_keys) and value.data_type != Type.ARRAY:
            keys_to_change.append(
                (
                    key,
                    Node(
                        data=[value],
                        data_type=Type.ARRAY,
                        start_column=value.start_column,
                        start_line=value.start_line,
                        end_column=value.end_column,
                        end_line=value.end_line,
                    ),
                )
            )
    for key, value in keys_to_change:
        stmt.data.pop(key)
        stmt.data.setdefault(key, value)
    return stmt


def patch_statement(stmt: Any | Node) -> Any | Node:
    # https://docs.aws.amazon.com/IAM/latest/UserGuide
    #   /reference_policies_elements_effect.html
    if isinstance(stmt, Node) and stmt.data_type == Type.OBJECT:
        stmt = patch_statement_node(stmt)
    elif isinstance(stmt, dict):
        stmt.setdefault("Effect", "Deny")

        for key in ("Action", "NotAction", "NotResource", "Resource"):
            if (key in stmt) and not isinstance(stmt[key], (list, UserList)):
                stmt[key] = [stmt[key]]
    return stmt


def yield_statements_from_policy(policy: Any | Node) -> Iterator[Any | Node]:
    if isinstance(policy, Node) and policy.inner.get("PolicyDocument", None):
        yield from yield_statements_from_policy_document(
            policy.inner.get("PolicyDocument")
        )
    elif hasattr(policy, "get") and policy.get("PolicyDocument", {}):
        yield from yield_statements_from_policy_document(
            policy.get("PolicyDocument")
        )


def yield_statements_from_policy_document(
    document: Any | Node,
) -> Iterator[Any | Node]:
    if (
        isinstance(document, Node)
        and hasattr(document.inner, "get")
        and document.inner.get("Statement", None)
    ):
        statement = document.inner.get("Statement", None)
        if isinstance(statement.inner, dict):
            yield patch_statement(statement)
        elif isinstance(statement.inner, list):
            yield from map(patch_statement, statement.data)
    else:
        if hasattr(document, "get"):
            statement = document.get("Statement", [])
        else:
            statement = []

        if isinstance(statement, dict):
            yield patch_statement(statement)
        elif isinstance(statement, (list, UserList)):
            yield from map(patch_statement, statement)
