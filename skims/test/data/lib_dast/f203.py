from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    policy = (
        "{"
        '"Version":"2008-10-17","Id":"LogPolicy",'
        '"Statement":['
        '{"Effect":"Allow",'
        '"Principal":{"policy":"*",},'
        '"Resource":["*",],},'
        "],"
        "}"
    )
    return {
        "Buckets": [
            {
                "Name": "fluidbucket",
            },
        ],
        "Grants": [
            {
                "Grantee": {
                    "DisplayName": "fluidattacks",
                    "EmailAddress": "fluid@fluidattacks.com",
                    "ID": "mygrant1",
                    "Type": "CanonicalUser",
                },
                "Permission": "FULL_CONTROL",
            },
        ],
        "Policy": policy,
    }
