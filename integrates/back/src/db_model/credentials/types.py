from db_model.enums import (
    CredentialType,
)
from typing import (
    List,
    NamedTuple,
    Union,
)


class CredentialMetadata(NamedTuple):
    type: CredentialType


class SshCredential(NamedTuple):
    key: str


class HttpsCredential(NamedTuple):
    user: str
    password: str


class HttpsCredentialToken(NamedTuple):
    token: str


class CredentialState(NamedTuple):
    modified_by: str
    modified_date: str
    name: str
    roots: List[str]
    value: Union[SshCredential, HttpsCredential, HttpsCredentialToken]


class CredentialItem(NamedTuple):
    group_name: str
    id: str
    metadata: CredentialMetadata
    state: CredentialState
