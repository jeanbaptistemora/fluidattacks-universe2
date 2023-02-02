from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Buckets": [
            {
                "Name": "unsafeBucket",
            },
        ],
        "Status": "Suspended",
        "MFADelete": "Disabled",
    }
