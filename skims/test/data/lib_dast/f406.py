from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "FileSystems": [
            {
                "FileSystemArn": "arn:aws:iam::123456789012:fs/fluidunsafe",
                "LifeCycleState": "available",
                "PerformanceMode": "generalPurpose",
                "Encrypted": False,
            },
            {
                "FileSystemArn": "arn:aws:iam::123456789012:fs/fluidsafe",
                "LifeCycleState": "available",
                "PerformanceMode": "generalPurpose",
                "Encrypted": True,
            },
        ],
    }
