# Standard library
from datetime import datetime

# Local libraries
from aws.model import (
    AWSIamPolicyStatement,
)
from parse_cfn.loader import (
    load_as_json,
    load_as_yaml,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents,
)


def test_iterate_iam_policy_documents_as_yml() -> None:
    expected = (
        AWSIamPolicyStatement(column=12, line=18, data={
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
        }),
        AWSIamPolicyStatement(column=12, line=24, data={
            'Action': [
                's3:GetObjectMetaData',
                's3:GetObject',
                's3:PutObject',
                's3:ListMultipartUploadParts',
                's3:AbortMultipartUpload',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=16, line=39, data={
            'Action': [
                'logs:CreateLogStream',
                'logs:CreateLogGroup',
                'logs:PutLogEvents',
            ],
            'Effect': 'Allow',
            'Resource': [
                'arn:aws:logs:*:*:*',
            ],
        }),
        AWSIamPolicyStatement(column=16, line=49, data={
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=12, line=62, data={
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=16, line=75, data={
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
        }),
        AWSIamPolicyStatement(column=14, line=84, data={
            'Action': ['sts:AssumeRole'],
            'Effect': 'Allow',
            'Resource': ['arn:aws:iam::*:role/cloud-lambda'],
        }),
    )

    with open('test/data/parse_cfn/full.yaml') as file:
        template = load_as_yaml(file.read())

    assert tuple(iterate_iam_policy_documents(template)) == expected


def test_iterate_iam_policy_documents_as_json() -> None:
    expected = (
        AWSIamPolicyStatement(column=15, line=18, data={
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
        }),
        AWSIamPolicyStatement(column=15, line=28, data={
            'Action': [
                's3:GetObjectMetaData',
                's3:GetObject',
                's3:PutObject',
                's3:ListMultipartUploadParts',
                's3:AbortMultipartUpload',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=19, line=50, data={
            'Action': [
                'logs:CreateLogStream',
                'logs:CreateLogGroup',
                'logs:PutLogEvents',
            ],
            'Effect': 'Allow',
            'Resource': [
                'arn:aws:logs:*:*:*',
            ],
        }),
        AWSIamPolicyStatement(column=19, line=68, data={
            'Action': [
                'comprehend:Detect*',
                'comprehend:BatchDetect*',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=15, line=89, data={
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
            ],
            'Effect': 'Allow',
            'Resource': ['*'],
        }),
        AWSIamPolicyStatement(column=19, line=109, data={
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
        }),
        AWSIamPolicyStatement(column=17, line=125, data={
            'Action': ['sts:AssumeRole'],
            'Effect': 'Allow',
            'Resource': ['arn:aws:iam::*:role/cloud-lambda'],
        }),
    )

    with open('test/data/parse_cfn/full.yaml.json') as file:
        template = load_as_json(file.read())

    assert tuple(iterate_iam_policy_documents(template)) == expected
