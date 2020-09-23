# Standard library
import re
from typing import (
    Any,
    Iterator,
)
from collections import (
    UserList,
)


def match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r'.*'.join(map(re.escape, pattern.split('*')))

    return bool(re.match(f'^{pattern}$', target, flags=flags))


def patch_statement(stmt: Any) -> Any:
    # https://docs.aws.amazon.com/IAM/latest/UserGuide
    #   /reference_policies_elements_effect.html

    if isinstance(stmt, dict):
        stmt.setdefault('Effect', 'Deny')

        for key in {'Action', 'NotAction', 'NotResource', 'Resource'}:
            if key in stmt:
                if not isinstance(stmt[key], (list, UserList)):
                    stmt[key] = [stmt[key]]

    return stmt


def yield_statements_from_policy(policy: Any) -> Iterator[Any]:
    document = policy.get('PolicyDocument', {})
    yield from yield_statements_from_policy_document(document)


def yield_statements_from_policy_document(document: Any) -> Iterator[Any]:
    statement = document.get('Statement', [])

    if isinstance(statement, dict):
        yield patch_statement(statement)
    elif isinstance(statement, (list, UserList)):
        yield from map(patch_statement, statement)
