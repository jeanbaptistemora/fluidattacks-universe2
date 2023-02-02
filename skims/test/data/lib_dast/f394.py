from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "trailList": [
            {
                "Name": "mytrail",
                "S3BucketName": "mybucket",
                "TrailARN": "arn:aws:iam::123456789012:mt/myTrail",
                "LogFileValidationEnabled": True,
                "IncludeGlobalServiceEvents": True,
                "IsMultiRegionTrail": True,
            },
        ]
    }
