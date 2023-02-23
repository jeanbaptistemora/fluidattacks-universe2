from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
)


class CredentialAttributesToAdd(NamedTuple):
    name: str
    key: str | None
    token: str | None
    type: CredentialType
    user: str | None
    password: str | None
    is_pat: bool | None = False
    azure_organization: str | None = None


class CredentialAttributesToUpdate(NamedTuple):
    name: str | None
    key: str | None
    token: str | None
    type: CredentialType | None
    user: str | None
    password: str | None
    is_pat: bool | None = False
    azure_organization: str | None = None
