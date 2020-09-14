# Standard library
from typing import (
    Any,
    Dict,
    Tuple,
)

# Local libraries
from parse_cfn.loader import (
    loads,
)


def iterate_resources(
    content: str,
    *expected_resource_kinds: str,
) -> Tuple[str, str, Dict[str, Any]]:
    template = loads(content)
    template_resources = template.get('Resources', {})

    for resource_name, resource_config in template_resources.items():
        if isinstance(resource_config, dict):
            resource_properties = resource_config['Properties']
            resource_kind = resource_config['Type']

            for expected_resource_kind in expected_resource_kinds:
                if resource_kind.startswith(expected_resource_kind):
                    yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_statements(content: str) -> Tuple[str, Dict[str, Any]]:
    for name, kind, props in iterate_resources(content, 'AWS::IAM'):
        if kind == 'AWS::IAM::Role':
            for policy in props.get('Policies', []):
                document = policy.get('PolicyDocument', {})
                yield name, document.get('Statement', [])
