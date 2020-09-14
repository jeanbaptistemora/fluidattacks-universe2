# Standard library
from typing import (
    Any,
    Dict,
    Iterator,
    Tuple,
)

# Local libraries
from parse_cfn.loader import (
    loads,
)


def iterate_resources(
    content: str,
    *expected_resource_kinds: str,
) -> Iterator[Tuple[str, str, Dict[str, Any]]]:
    template = loads(content)
    template_resources = template.get('Resources', {})

    for resource_name, resource_config in template_resources.items():
        if isinstance(resource_config, dict):
            resource_properties = resource_config['Properties']
            resource_kind = resource_config['Type']

            for expected_resource_kind in expected_resource_kinds:
                if resource_kind.startswith(expected_resource_kind):
                    yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_statements(content: str) -> Iterator[Dict[str, Any]]:

    def _yield_statements_from_policy(policy: Any) -> Iterator[Any]:
        document = policy.get('PolicyDocument', {})
        for statement in document.get('Statement', []):
            yield statement

    for _, kind, props in iterate_resources(content, 'AWS::IAM'):

        if kind in {'AWS::IAM::ManagedPolicy', 'AWS::IAM::Policy'}:
            yield from _yield_statements_from_policy(props)

        if kind in {'AWS::IAM::Role', 'AWS::IAM::User'}:
            for policy in props.get('Policies', []):
                yield from _yield_statements_from_policy(policy)
