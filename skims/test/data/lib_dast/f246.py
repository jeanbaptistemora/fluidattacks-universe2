from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "DBInstances": [
            {
                "DBInstanceArn": "arn:aws:iam::123456789012:db/unsafedb",
                "StorageEncrypted": False,
            },
            {
                "DBInstanceArn": "arn:aws:iam::123456789012:db/safedb",
                "StorageEncrypted": True,
            },
        ],
    }
