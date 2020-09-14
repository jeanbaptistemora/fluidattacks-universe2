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
        ('AWSManagedPolicy1', [{
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': {
                'Fn::Sub': 'arn:aws:s3:::${pS3RestoreBucket}',
                '__column__': 12,
                '__line__': 22,
            },
            '__column__': 10,
            '__line__': 17,
        }, {
            'Action': [
                's3:GetObjectMetaData',
                's3:GetObject',
                's3:PutObject',
                's3:ListMultipartUploadParts',
                's3:AbortMultipartUpload',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 10,
            '__line__': 23,
        }]),
        ('AWSIamRole1', [{
            'Action': [
                'logs:CreateLogStream',
                'logs:CreateLogGroup',
                'logs:PutLogEvents',
            ],
            'Effect': 'Allow',
            'Resource': [
                'arn:aws:logs:*:*:*',
            ],
            '__column__': 12,
            '__line__': 38,
        }]),
        ('AWSIamRole1', [{
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 12,
            '__line__': 48,
        }]),
        ('AWSPolicy1', [{
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 12,
            '__line__': 61,
        }]),
    )
