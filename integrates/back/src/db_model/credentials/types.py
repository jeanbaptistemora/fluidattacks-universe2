from db_model.enums import (
    CredentialType,
)
from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class CredentialMetadata(NamedTuple):
    type: CredentialType


class CredentialState(NamedTuple):
    modified_by: str
    modified_date: str
    name: str
    roots: List[str]
    key: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None


class CredentialItem(NamedTuple):
    group_name: str
    id: str
    metadata: CredentialMetadata
    state: CredentialState


# New types
class HttpsSecret(NamedTuple):
    user: str
    password: str


class HttpsPatSecret(NamedTuple):
    token: str


class SshSecret(NamedTuple):
    key: str


class CredentialNewState(NamedTuple):
    modified_by: str
    modified_date: str
    name: str
    type: CredentialType
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret]


class Credential(NamedTuple):
    id: str
    organization_id: str
    owner: str
    state: CredentialNewState


class CredentialRequest(NamedTuple):
    id: str
    organization_id: str
