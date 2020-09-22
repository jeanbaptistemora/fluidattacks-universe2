# Third party libraries
from lark import (
    Tree,
)
from lark.lexer import (
    Token,
)

# Local libraries
from parse_hcl2.loader import (
    blocking_load,
)
from parse_hcl2.structure import (
    IamPolicyStatement,
    iterate_iam_policy_documents,
    iterate_resources,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
)


def test_iterate_resources() -> None:
    with open('test/data/parse_hcl2/iam.tf') as file:
        model = blocking_load(file.read())

    assert len(tuple(iterate_resources(model, 'resource', 'aws_iam_role'))) == 1


def test_iterate_iam_policy_documents() -> None:
    with open('test/data/parse_hcl2/iam.tf') as file:
        model = blocking_load(file.read())

    assert tuple(iterate_iam_policy_documents(model)) == (
        IamPolicyStatement(
            column=23,
            data={
                'Action': ['sts:AssumeRole'],
                'Principal': {
                    'Service': 'ec2.amazonaws.com',
                },
                'Effect': 'Allow',
            },
            line=5,
        ),
        IamPolicyStatement(
            column=11,
            data={
                'Action': ['ec2:Describe*'],
                'Effect': 'Allow',
                'Resource': ['*'],
            },
            line=25,
        ),
    )
