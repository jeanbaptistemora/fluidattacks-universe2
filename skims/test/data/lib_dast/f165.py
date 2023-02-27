from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    content = (
        b"arn,access_key_1_active,access_key_2_active,cert_1_active\n"
        b"myUser,true,true,true"
    )
    return {
        "Users": [
            {
                "UserName": "myUser",
                "UserId": "1234",
                "Arn": "arn:aws:iam::123456789012:user/myUser",
            },
        ],
        "AccessKeyMetadata": [
            {
                "UserName": "myUser",
                "AccessKeyId": "108745",
                "Status": "Active",
            },
            {
                "UserName": "myUser",
                "AccessKeyId": "37856",
                "Status": "Active",
            },
        ],
        "State": "STARTED",
        "Description": "string",
        "Content": content,
        "ReportFormat": "text/csv",
        "PolicyGroups": [],
        "PolicyUsers": [],
        "PolicyRoles": [],
        "TableNames": [
            "fluidTable",
        ],
        "Table": {
            "TableName": "fluidTable",
            "TableArn": "arn:aws:iam::aws:table/fluidTable",
            "SSEDescription": {
                "Status": "ENABLED",
                "SSEType": "AES256",
                "KMSMasterKeyArn": "arn:aws:iam::aws:key/fuildKey",
            },
        },
    }
