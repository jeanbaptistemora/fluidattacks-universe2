from datetime import (
    datetime,
)
from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
    Optional,
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
    modified_date: datetime
    name: str
    type: CredentialType
    is_pat: bool
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret]
    azure_organization: Optional[str] = None


class Credentials(NamedTuple):
    id: str
    organization_id: str
    owner: str
    state: CredentialsState


class CredentialsRequest(NamedTuple):
    id: str
    organization_id: str
