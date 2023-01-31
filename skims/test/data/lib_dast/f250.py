from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Volumes": [
            {
                "Encrypted": False,
                "KmsKeyId": "string",
                "OutpostArn": "arn:aws:iam::123456789012:out/myout",
                "Size": 1,
                "State": "available",
                "VolumeId": "myVolume123",
                "VolumeType": "io1",
            },
        ],
    }
