import base64
import binascii
from custom_exceptions import (
    InvalidBase64SshKey,
)
from db_model.credentials.types import (
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from typing import (
    Union,
)


def format_credentials_ssh_key(ssh_key: str) -> str:
    try:
        raw_ssh_key: str = base64.b64decode(ssh_key, validate=True).decode()
    except binascii.Error as exc:
        raise InvalidBase64SshKey() from exc

    if not raw_ssh_key.endswith("\n"):
        raw_ssh_key += "\n"
    encoded_ssh_key = base64.b64encode(raw_ssh_key.encode()).decode()

    return encoded_ssh_key


def format_credentials_secret_type(
    item: dict[str, str]
) -> Union[HttpsSecret, HttpsPatSecret, SshSecret]:
    credential_type = CredentialType(item["type"])
    return (
        SshSecret(key=format_credentials_ssh_key(item["key"]))
        if credential_type is CredentialType.SSH
        else HttpsPatSecret(token=item["token"])
        if "token" in item
        else HttpsSecret(
            user=item["user"],
            password=item["password"],
        )
    )
