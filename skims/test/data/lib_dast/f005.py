from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    policy = (
        "{"
        '"Version":"2008-10-17","Id":"LogPolicy",'
        '"Statement":['
        '{"Effect":"Allow",'
        '"Action":["iam:CreatePolicyVersion","iam:SetDefaultPolicyVersion",'
        '"iam:AttachUserPolicy",],'
        '"Resource":["arn:aws:s3:::policytest1/*",],},'
        "],"
        "}"
    )
    return {
        "Policies": [
            {
                "PolicyId": "pol-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:policy/mypolicy",
                "DefaultVersionId": "pol-018de572ae43404d8",
                "AttachmentCount": 123,
                "PermissionsBoundaryUsageCount": 123,
                "IsAttachable": False,
                "Description": "string",
            },
        ],
        "PolicyVersion": {
            "Document": policy,
            "VersionId": "fluidversion",
            "IsDefaultVersion": False,
        },
    }
