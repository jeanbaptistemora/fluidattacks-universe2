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
    }
