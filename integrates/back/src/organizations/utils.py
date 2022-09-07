# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    if credential_type is CredentialType.HTTPS:
        if item.get("token"):
            return HttpsPatSecret(token=item["token"])
        return HttpsSecret(user=item["user"], password=item["password"])
    return SshSecret(key=format_credentials_ssh_key(item["key"]))
