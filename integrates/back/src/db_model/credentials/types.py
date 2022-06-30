from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
    Union,
)


class HttpsSecret(NamedTuple):
    user: str
    password: str


class HttpsPatSecret(NamedTuple):
    token: str


class SshSecret(NamedTuple):
    key: str


class CredentialsState(NamedTuple):
    modified_by: str
    modified_date: str
    name: str
    type: CredentialType
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret]


class Credentials(NamedTuple):
    id: str
    organization_id: str
    owner: str
    state: CredentialsState


class CredentialsRequest(NamedTuple):
    id: str
    organization_id: str
