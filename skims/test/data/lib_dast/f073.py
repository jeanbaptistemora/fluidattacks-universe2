from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb12",
                "DBInstanceArn": "arn:aws:iam::123456789012:db/unsafedb",
                "PubliclyAccessible": True,
            },
            {
                "DBInstanceIdentifier": "mydb12",
                "DBInstanceArn": "arn:aws:iam::123456789012:db/safedb",
                "PubliclyAccessible": False,
            },
        ],
        "DBClusters": [
            {
                "DBClusterArn": "arn:aws:iam::123456789012:dbc/unsafe",
                "PubliclyAccessible": True,
            },
            {
                "DBClusterArn": "arn:aws:iam::123456789012:dbc/safe",
                "PubliclyAccessible": False,
            },
        ],
    }
