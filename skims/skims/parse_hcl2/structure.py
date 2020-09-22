# Standard library
from itertools import (
    chain,
)
from typing import (
    Any,
    Iterator,
    NamedTuple,
    Optional,
)

# Third party libraries
from lark import (
    Tree,
)

# Local libraries
from aws.iam.utils import (
    yield_statements_from_policy_document,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
    Json,
)


def get_block_attribute(block: Block, key: str) -> Optional[Attribute]:
    for attribute in iterate_block_attributes(block):
        if attribute.key == key:
            return attribute
    return None


def iterate_resources(
    model: Any,
    expected_source: str,
    *expected_kinds: str,
) -> Iterator[Block]:
    if isinstance(model, Tree):
        for child in model.children:
            yield from iterate_resources(
                child,
                expected_source,
                *expected_kinds,
            )
    elif isinstance(model, Block) and (
        len(model.namespace) == 3
        and model.namespace[0] == expected_source
        and model.namespace[1] in expected_kinds
    ):
        yield model


def iterate_block_attributes(block: Block) -> Iterator[Attribute]:
    for item in block.body:
        if isinstance(item, Attribute):
            yield item


IamPolicyStatement = NamedTuple('IamPolicyStatement', [
    ('column', int),
    ('data', Any),
    ('line', int),
])


def iterate_iam_policy_documents(
    model: Any,
) -> Iterator[IamPolicyStatement]:
    for iterator in (
        _iterate_iam_policy_documents_from_resource_with_assume_role_policy,
        _iterate_iam_policy_documents_from_resource_with_policy,
    ):
        yield from iterator(model)


def _iterate_iam_policy_documents_from_resource_with_assume_role_policy(
    model: Any,
) -> Iterator[IamPolicyStatement]:
    for resource in iterate_resources(model, 'resource', 'aws_iam_role'):
        attribute = get_block_attribute(resource, 'assume_role_policy')
        yield from _yield_statements_from_policy_document_attribute(attribute)


def _iterate_iam_policy_documents_from_resource_with_policy(
    model: Any,
) -> Iterator[IamPolicyStatement]:
    for res in chain(
        iterate_resources(model, 'resource', 'aws_iam_group_policy'),
        iterate_resources(model, 'resource', 'aws_iam_policy'),
        iterate_resources(model, 'resource', 'aws_iam_role_policy'),
        iterate_resources(model, 'resource', 'aws_iam_user_policy'),
    ):
        attribute = get_block_attribute(res, 'policy')
        yield from _yield_statements_from_policy_document_attribute(attribute)


def _yield_statements_from_policy_document_attribute(
    attribute: Any,
) -> Iterator[IamPolicyStatement]:
    if attribute and isinstance(attribute.val, Json):
        data = attribute.val
        for stmt in yield_statements_from_policy_document(data.data):
            yield IamPolicyStatement(
                column=data.column,
                data=stmt,
                line=data.line,
            )
