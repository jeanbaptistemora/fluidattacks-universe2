from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    policy = (
        "{"
        '"Version":"2008-10-17","Id":"LogPolicy",'
        '"Statement":'
        "["
        "{"
        '"Effect":"Allow",'
        '"Action":["iam:CreatePolicyVersion",],'
        '"Resource":["arn:aws:s3:::policytest1/*",],'
        '"Condition":{"Bool":{"aws:SecureTransport": "false",},},'
        "},"
        "{"
        '"Effect":"Deny",'
        '"Action":["iam:CreatePolicyVersion",],'
        '"Resource":["arn:aws:s3:::policytest1/*",],'
        '"Condition":{"Bool":{"aws:SecureTransport": "true",},},'
        "},"
        "],"
        "}"
    )
    return {
        "Buckets": [
            {
                "Name": "fluidattacksSCA",
            },
        ],
        "Policy": policy,
    }
