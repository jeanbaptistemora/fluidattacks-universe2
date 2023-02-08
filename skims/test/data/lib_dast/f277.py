from datetime import (
    datetime,
)
from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    date = datetime.fromisoformat("2022-11-01T04:16:13-04:00")
    return {
        "Users": [
            {
                "UserName": "fluidattacks",
                "Arn": "arn:aws:iam::123456789012:user/fluid",
            },
        ],
        "SSHPublicKeys": [
            {
                "UserName": "fluidattacks",
                "SSHPublicKeyId": "ssh:42673",
                "Status": "Active",
                "UploadDate": date,
            },
        ],
    }
