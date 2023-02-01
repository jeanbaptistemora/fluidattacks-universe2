from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    policy = (
        '{"Version":"2008-10-17","Id":"LogPolicy",'
        '"Statement":[{"Condition":{"Null":'
        '{"s3:x-amz-server-side-encryption": "false",},},'
        '"Effect":"Allow","Principal":{"AWS":"111122223333"},'
        '"Action":["s3:GetBucketAcl","s3:GetObjectAcl","s3:PutObject"],'
        '"Resource":["arn:aws:s3:::policytest1/*",]}]}'
    )
    return {
        "Buckets": [
            {
                "Name": "myBucket1",
            },
        ],
        "Policy": policy,
    }
