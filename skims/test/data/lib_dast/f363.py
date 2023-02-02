from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "PasswordPolicy": {
            "MinimumPasswordLength": 10,
            "RequireSymbols": False,
            "RequireNumbers": False,
            "RequireUppercaseCharacters": False,
            "RequireLowercaseCharacters": False,
            "MaxPasswordAge": 100,
            "PasswordReusePrevention": 20,
            "AllowUsersToChangePassword": False,
            "ExpirePasswords": False,
            "HardExpiry": False,
        },
        "User": {
            "UserName": "fluidattacks",
            "UserId": "fluid123",
            "Arn": "arn:aws:iam::123456789012:user/fluidAttacks",
        },
    }
