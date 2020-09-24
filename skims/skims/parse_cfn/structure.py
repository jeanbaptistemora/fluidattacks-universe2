# Standard library
from typing import (
    Any,
    Dict,
    Iterator,
    Tuple,
)

# Local libraries
from aws.iam.utils import (
    yield_statements_from_policy,
    yield_statements_from_policy_document,
)
from aws.model import (
    AWSIamPolicyStatement,
    AWSIamManagedPolicyArns,
)


def iterate_resources(
    template: Any,
    *expected_resource_kinds: str,
) -> Iterator[Tuple[str, str, Dict[str, Any]]]:
    if not isinstance(template, dict):
        return

    template_resources = template.get('Resources', {})

    for resource_name, resource_config in template_resources.items():
        if isinstance(resource_config, dict) \
                and 'Properties' in resource_config \
                and 'Type' in resource_config:
            resource_properties = resource_config['Properties']
            resource_kind = resource_config['Type']

            for expected_resource_kind in expected_resource_kinds:
                if resource_kind.startswith(expected_resource_kind):
                    yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_documents(
    template: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for statement in _iterate_iam_policy_documents(template):
        yield AWSIamPolicyStatement(
            column=statement.pop('__column__'),
            data=statement,
            line=statement.pop('__line__'),
        )


def _iterate_iam_policy_documents(
    template: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for _, kind, props in iterate_resources(template, 'AWS::IAM'):

        if kind in {'AWS::IAM::ManagedPolicy', 'AWS::IAM::Policy'}:
            yield from yield_statements_from_policy(props)

        if kind in {'AWS::IAM::Role', 'AWS::IAM::User'}:
            for policy in props.get('Policies', []):
                yield from yield_statements_from_policy(policy)

        if kind in {'AWS::IAM::Role'}:
            document = props.get('AssumeRolePolicyDocument', {})
            yield from yield_statements_from_policy_document(document)


def iterate_managed_policy_arns(
    template: Any,
) -> Iterator[AWSIamManagedPolicyArns]:
    for _, _, props in iterate_resources(template, 'AWS::IAM'):
        if policies := props.get('ManagedPolicyArns', None):
            yield AWSIamManagedPolicyArns(
                column=policies.__column__,
                data=policies,
                line=policies.__line__,
            )
