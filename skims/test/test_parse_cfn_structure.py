# Standard library
from datetime import datetime

# Local libraries
from parse_cfn.loader import (
    loads,
)
from parse_cfn.structure import (
    iterate_iam_policy_statements,
)


def test_iterate_iam_policy_statements() -> None:
    with open('test/data/parse_cfn/full.yaml') as file:
        content = file.read()

    assert tuple(iterate_iam_policy_statements(content)) == (
        ('AWSIamRole1', [{
            'Action': [
                'logs:CreateLogStream',
                'logs:CreateLogGroup',
                'logs:PutLogEvents',
            ],
            'Effect': 'Allow',
            'Resource': ['arn:aws:logs:*:*:*'],
            '__column__': 12,
            '__line__': 17,
        }]),
        ('AWSIamRole1', [{
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 12,
            '__line__': 27,
        }]),
    )
