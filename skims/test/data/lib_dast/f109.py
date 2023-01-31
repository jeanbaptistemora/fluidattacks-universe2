from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb12",
                "DBInstanceArn": "arn:aws:iam::123456789012:db/mydb",
            }
        ],
        "DBClusters": [
            {
                "DBClusterArn": "arn:aws:iam::123456789012:dbc/mydbcluster",
            }
        ],
    }
