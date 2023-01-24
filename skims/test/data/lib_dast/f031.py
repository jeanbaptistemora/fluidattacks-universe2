from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Policies": [
            {
                "PolicyName": "unsafePol",
                "PolicyId": "pol-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:policy/AdministratorAccess",
                "Path": "server-certificate/ProdServerCert",
                "DefaultVersionId": "pol-018",
                "AttachmentCount": 1,
                "PermissionsBoundaryUsageCount": 1,
                "IsAttachable": True,
                "Description": "string",
                "CreateDate": "2015/01/01",
                "UpdateDate": "2015/01/01",
            },
        ],
        "IsTruncated": True,
        "Marker": "4f23ro",
        "Buckets": [
            {
                "Name": "bucket-018de572ae43404d8",
            }
        ],
        "Owner": {"DisplayName": "string", "ID": "string"},
        "Grants": [
            {
                "Grantee": {
                    "DisplayName": "string",
                    "EmailAddress": "string",
                    "ID": "string",
                    "Type": "CanonicalUser",
                    "URI": "http://acs.amazonaws.com/groups/global/AllUsers",
                },
                "Permission": "FULL_CONTROL",
            },
        ],
        "PolicyNames": [
            "inlinePolicy1",
        ],
        "Users": [
            {
                "UserName": "bucket-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:user/user1",
            }
        ],
        "AttachedPolicies": [
            {"PolicyName": "inlinePolicy1", "PolicyArn": "policyArn"},
        ],
    }
