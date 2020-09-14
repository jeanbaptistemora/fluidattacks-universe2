# Standard library
from datetime import datetime

# Local libraries
from parse_cfn.loader import (
    load_as_yaml,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents,
)


def test_iterate_iam_policy_documents() -> None:
    expected = (
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': {
                'Fn::Sub': 'arn:aws:s3:::${pS3RestoreBucket}',
                '__column__': 14,
                '__line__': 22,
            },
            '__column__': 12,
            '__line__': 17,
        },
        {
            'Action': [
                's3:GetObjectMetaData',
                's3:GetObject',
                's3:PutObject',
                's3:ListMultipartUploadParts',
                's3:AbortMultipartUpload',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 12,
            '__line__': 23,
        },
        {
            'Action': [
                'logs:CreateLogStream',
                'logs:CreateLogGroup',
                'logs:PutLogEvents',
            ],
            'Effect': 'Allow',
            'Resource': [
                'arn:aws:logs:*:*:*',
            ],
            '__column__': 16,
            '__line__': 38,
        },
        {
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 16,
            '__line__': 48,
        },
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': '*',
            '__column__': 12,
            '__line__': 61,
        },
        {
            'Action': '*',
            'Condition': {
                'StringNotEquals': {
                    '__column__': 20,
                    '__line__': 79,
                    'aws:RequestedRegion': 'us-east-1',
                },
                '__column__': 18,
                '__line__': 78,
            },
            'Effect': 'Deny',
            'Resource': '*',
            '__column__': 16,
            '__line__': 74,
        },
        {
            'Action': 'sts:AssumeRole',
            'Effect': 'Allow',
            'Resource': 'arn:aws:iam::*:role/cloud-lambda',
            '__column__': 16,
            '__line__': 80,
        },
    )

    with open('test/data/parse_cfn/full.yaml') as file:
        template = load_as_yaml(file.read())

    assert tuple(iterate_iam_policy_documents(template)) == expected
