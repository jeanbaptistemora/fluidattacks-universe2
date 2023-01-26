from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    document = (
        "{'Statement':[{'Effect': 'Allow', 'Action': '*', 'Resource': '*'},"
        "{'Effect': 'Allow', 'Resource': '*', 'Action': '*',},"
        "{'Effect': 'Allow', 'NotAction': ['w',], 'NotResource': ['w',]} ],}"
    )

    return {
        "Policies": [
            {
                "PolicyName": "myPolicy",
                "PolicyId": "pol-018de572ae43404d8",
                "Arn": "arn:aws:iam::123456789012:policy/myPolicy",
                "DefaultVersionId": "v1",
            },
        ],
        "PolicyVersion": {
            "Document": document,
            "VersionId": "v1",
            "IsDefaultVersion": True,
        },
        "Aliases": [
            {
                "AliasName": "myAlias",
                "AliasArn": "arn:aws:iam::123456789012:alias/",
                "TargetKeyId": "mykeyId",
            },
        ],
        "PolicyNames": [
            "myPolicy",
        ],
        "Policy": "{'Statement': [{'Principal': {'AWS': '*'},},],}",
    }
