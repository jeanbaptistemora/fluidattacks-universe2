# Third party libraries
from lark import (
    Tree,
)
from lark.lexer import (
    Token,
)

# Local libraries
from parse_hcl2.loader import (
    load,
)
from parse_hcl2.structure import (
    iterate_iam_policy_documents,
    iterate_resources,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
    Json,
)


def test_iterate_resources() -> None:
    with open('test/data/parse_hcl2/iam.tf') as file:
        model = load(file.read())

    assert len(tuple(iterate_resources(model, 'resource', 'aws_iam_role'))) == 1


def test_iterate_iam_policy_documents() -> None:
    with open('test/data/parse_hcl2/iam.tf') as file:
        model = load(file.read())

    assert tuple(iterate_iam_policy_documents(model)) == (
        Json(
            column=23,
            data={
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'sts:AssumeRole',
                    'Principal': {
                        'Service': 'ec2.amazonaws.com',
                    },
                    'Effect': 'Allow',
                }],
            },
            line=5,
        ),
    )
