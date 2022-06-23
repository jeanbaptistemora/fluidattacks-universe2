from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
    Optional,
)


class CredentialAttributesToAdd(NamedTuple):
    name: str
    key: Optional[str]
    token: Optional[str]
    type: CredentialType
    user: Optional[str]
    password: Optional[str]


class CredentialAttributesToUpdate(NamedTuple):
    name: Optional[str]
    key: Optional[str]
    token: Optional[str]
    type: Optional[CredentialType]
    user: Optional[str]
    password: Optional[str]
