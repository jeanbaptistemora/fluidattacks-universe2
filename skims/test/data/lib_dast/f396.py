from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Keys": [
            {"KeyId": "123", "KeyArn": "arn:aws:iam::123456789012:key/myKey"},
        ],
        "KeyRotationEnabled": False,
    }
