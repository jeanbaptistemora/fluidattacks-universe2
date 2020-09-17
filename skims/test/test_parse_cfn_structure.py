# Standard library
from datetime import datetime

# Local libraries
from parse_cfn.loader import (
    load_as_json,
    load_as_yaml,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents,
)


def test_iterate_iam_policy_documents_as_yml() -> None:
    expected = (
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': [{
                'Fn::Sub': 'arn:aws:s3:::${pS3RestoreBucket}',
                '__column__': 14,
                '__line__': 23,
            }],
            '__column__': 12,
            '__line__': 18,
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
            'Resource': ['*'],
            '__column__': 12,
            '__line__': 24,
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
            '__line__': 39,
        },
        {
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
            '__column__': 16,
            '__line__': 49,
        },
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
            '__column__': 12,
            '__line__': 62,
        },
        {
            'Action': ['*'],
            'Condition': {
                'StringNotEquals': {
                    '__column__': 20,
                    '__line__': 80,
                    'aws:RequestedRegion': 'us-east-1',
                },
                '__column__': 18,
                '__line__': 79,
            },
            'Effect': 'Deny',
            'Resource': ['*'],
            '__column__': 16,
            '__line__': 75,
        },
        {
            'Action': ['sts:AssumeRole'],
            'Effect': 'Allow',
            'Resource': ['arn:aws:iam::*:role/cloud-lambda'],
            '__column__': 14,
            '__line__': 84,
        },
    )

    with open('test/data/parse_cfn/full.yaml') as file:
        template = load_as_yaml(file.read())

    assert tuple(iterate_iam_policy_documents(template)) == expected


def test_iterate_iam_policy_documents_as_json() -> None:
    expected = (
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': [{
                'Fn::Sub': 'arn:aws:s3:::${pS3RestoreBucket}',
                '__column__': 17,
                '__line__': 24,
            }],
            '__column__': 15,
            '__line__': 18,
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
            'Resource': ['*'],
            '__column__': 15,
            '__line__': 28,
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
            '__column__': 19,
            '__line__': 50,
        },
        {
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
            '__column__': 19,
            '__line__': 68,
        },
        {
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
            '__column__': 15,
            '__line__': 89,
        },
        {
            'Action': ['*'],
            'Condition': {
                'StringNotEquals': {
                    '__column__': 23,
                    '__line__': 114,
                    'aws:RequestedRegion': 'us-east-1',
                },
                '__column__': 21,
                '__line__': 113,
            },
            'Effect': 'Deny',
            'Resource': ['*'],
            '__column__': 19,
            '__line__': 109,
        },
        {
            'Action': ['sts:AssumeRole'],
            'Effect': 'Allow',
            'Resource': ['arn:aws:iam::*:role/cloud-lambda'],
            '__column__': 17,
            '__line__': 125,
        },
    )

    with open('test/data/parse_cfn/full.yaml.json') as file:
        template = load_as_json(file.read())

    assert tuple(iterate_iam_policy_documents(template)) == expected
