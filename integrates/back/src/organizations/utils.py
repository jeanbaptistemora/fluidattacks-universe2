import base64
import binascii
from custom_exceptions import (
    InvalidBase64SshKey,
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
