from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:

    return {
        "TableNames": [
            "fluidbackup",
        ],
        "ContinuousBackupsDescription": {
            "ContinuousBackupsStatus": "DISABLED",
            "PointInTimeRecoveryDescription": {
                "PointInTimeRecoveryStatus": "DISABLED",
            },
        },
        "Table": {
            "TableName": "fluidbackup",
            "TableArn": "arn:aws:iam::123456789012:db/fluiddb",
        },
    }
