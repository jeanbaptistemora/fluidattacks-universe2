from datetime import (
    datetime,
)
from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    date = datetime.fromisoformat("2022-11-01T04:16:13-04:00")
    content = (
        "user,arn,password_enabled,access_key_1_active,access_key_2_active,"
        "access_key_1_last_rotated,access_key_2_last_rotated\n"
        f"fluid,arn:aws:iam::myUser,true,true,true,{date},{date}"
    )
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
        "Content": bytes(content, "utf-8"),
        "User": {
            "PasswordLastUsed": date,
        },
    }
