from db_model.enums import (
    CredentialType,
)
from typing import (
    List,
    NamedTuple,
    Optional,
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
