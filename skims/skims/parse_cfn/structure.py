# Standard library
from typing import (
    Any,
    Dict,
    Iterator,
    Tuple,
)


def iterate_resources(
    template: Any,
    *expected_resource_kinds: str,
) -> Iterator[Tuple[str, str, Dict[str, Any]]]:
    template_resources = template.get('Resources', {})

    for resource_name, resource_config in template_resources.items():
        if isinstance(resource_config, dict):
            resource_properties = resource_config['Properties']
            resource_kind = resource_config['Type']

            for expected_resource_kind in expected_resource_kinds:
                if resource_kind.startswith(expected_resource_kind):
                    yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_documents(template: Any) -> Iterator[Dict[str, Any]]:

    def _yield_statements_from_policy(policy: Any) -> Iterator[Any]:
        document = policy.get('PolicyDocument', {})
        statement = document.get('Statement', [])

        if isinstance(statement, dict):
            yield _patch_statement(statement)
        elif isinstance(statement, list):
            yield from map(_patch_statement, statement)

    for _, kind, props in iterate_resources(template, 'AWS::IAM'):

        if kind in {'AWS::IAM::ManagedPolicy', 'AWS::IAM::Policy'}:
            yield from _yield_statements_from_policy(props)

        if kind in {'AWS::IAM::Role', 'AWS::IAM::User'}:
            for policy in props.get('Policies', []):
                yield from _yield_statements_from_policy(policy)


def _patch_statement(stmt: Any) -> Iterator[Any]:
    if isinstance(stmt, dict):
        for key in {'Action', 'NotAction', 'NotResource', 'Resource'}:
            if key in stmt:
                if not isinstance(stmt[key], list):
                    stmt[key] = [stmt[key]]

    return stmt
