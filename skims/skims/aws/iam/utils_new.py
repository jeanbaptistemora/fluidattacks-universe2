# Standard library
import re
from typing import (
    Iterator,
)

# Local libraries
from metaloaders.model import (
    Node,
    Type as Type,
)


def match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r'.*'.join(map(re.escape, pattern.split('*')))

    return bool(re.match(f'^{pattern}$', target, flags=flags))


def patch_statement(stmt: Node) -> Node:
    # https://docs.aws.amazon.com/IAM/latest/UserGuide
    #   /reference_policies_elements_effect.html

    if stmt.data_type == Type.OBJECT:
        stmt.inner.setdefault('Effect', 'Deny')
        allow_keys = {'Action', 'NotAction', 'NotResource', 'Resource'}
        keys_to_change = []
        for key, value in stmt.data.items():
            if key.inner in allow_keys:
                if not value.data_type == Type.ARRAY:
                    keys_to_change.append((
                        key,
                        Node(
                            data=[value],
                            data_type=Type.ARRAY,
                            start_column=value.start_column,
                            start_line=value.start_line,
                            end_column=value.end_column,
                            end_line=value.end_line,
                        ),
                    ))
        for key, value in keys_to_change:
            stmt.data.pop(key)
            stmt.data.setdefault(key, value)

    return stmt


def yield_statements_from_policy(policy: Node) -> Iterator[Node]:
    if document := policy.inner.get('PolicyDocument', None):
        yield from yield_statements_from_policy_document(document)


def yield_statements_from_policy_document(document: Node) -> Iterator[Node]:
    if statement := document.inner.get('Statement', None):
        if isinstance(statement.inner, dict):
            yield patch_statement(statement)
        elif isinstance(statement.inner, list):
            yield from map(patch_statement, statement.data)
