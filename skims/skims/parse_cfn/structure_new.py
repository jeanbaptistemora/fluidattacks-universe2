# Standard library
from typing import (
    Any,
    Iterator,
    Tuple,
)

# Third party libraries
from metaloaders.model import Node, Type

# Local libraries
from aws.iam.utils_new import (
    yield_statements_from_policy,
    yield_statements_from_policy_document,
)


def iterate_resources(
    template: Node,
    *expected_resource_kinds: str,
) -> Iterator[Tuple[Node, Node, Node]]:
    if not isinstance(template, Node):
        return

    if template_resources := template.inner.get('Resources', None):
        for resource_name, resource_config in template_resources.data.items():
            if resource_config.data_type == Type.OBJECT \
                    and 'Properties' in resource_config.inner \
                    and 'Type' in resource_config.inner:
                resource_properties = resource_config.inner['Properties']
                resource_kind = resource_config.inner['Type']

                for expected_resource_kind in expected_resource_kinds:
                    if resource_kind.inner.startswith(expected_resource_kind):
                        yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_documents(
    template: Node,
) -> Iterator[Node]:
    for _, kind, props in iterate_resources(template, 'AWS::IAM'):

        if kind.inner in {'AWS::IAM::ManagedPolicy', 'AWS::IAM::Policy'}:
            yield from yield_statements_from_policy(props)

        if kind.inner in {'AWS::IAM::Role', 'AWS::IAM::User'}:
            if policies := props.inner.get('Policies', None):
                for policy in policies.data:
                    yield from yield_statements_from_policy(policy)

        if kind.inner in {'AWS::IAM::Role'}:
            if document := props.inner.get('AssumeRolePolicyDocument', None):
                yield from yield_statements_from_policy_document(document)


def iterate_managed_policy_arns(
    template: Any,
) -> Iterator[Node]:
    for _, _, props in iterate_resources(template, 'AWS::IAM'):
        if policies := props.inner.get('ManagedPolicyArns', None):
            yield policies
