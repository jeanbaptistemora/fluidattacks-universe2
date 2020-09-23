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
            column=2,
            data={
                'actions': [
                    's3:ListAllMyBuckets',
                    's3:GetBucketLocation',
                ],
                'sid': '1',
                'resources': [
                    'arn:aws:s3:::*',
                ],
            },
            line=103,
        ),
        IamPolicyStatement(
            column=2,
            data={
                'actions': ['s3:ListBucket'],
                'resources': ['arn:aws:s3:::${var.s3_bucket_name}'],
            },
            line=116,
        ),
        IamPolicyStatement(
            column=2,
            data={
                'actions': [
                    's3:*',
                ],
                'resources': [
                    'arn:aws:s3:::${var.s3_bucket_name}/home/&{aws:username}',
                    'arn:aws:s3:::${var.s3_bucket_name}/home/&{aws:username}/*',
                ],
            },
            line=137,
        ),
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
            line=45,
        ),
        IamPolicyStatement(
            column=11,
            data={
                'Action': ['ec2:Describe*'],
                'Effect': 'Allow',
                'Resource': ['*'],
            },
            line=66,
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
        IamPolicyStatement(
            column=11,
            data={
                'Action': ['ec2:Describe*'],
                'Effect': 'Allow',
                'Resource': ['*'],
            },
            line=86,
        ),
    )
