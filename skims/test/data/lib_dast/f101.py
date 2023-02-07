from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Buckets": [
            {
                "Name": "fluidbucket",
            },
        ],
        "ObjectLockConfiguration": {
            "ObjectLockEnabled": "Disabled",
            "Rule": {
                "DefaultRetention": {
                    "Mode": "GOVERNANCE",
                    "Days": 1,
                    "Years": 1,
                }
            },
        },
    }
