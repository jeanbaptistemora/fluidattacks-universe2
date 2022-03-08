from db_model.enums import (
    CredentialType,
)
from typing import (
    List,
    NamedTuple,
)


class CredentialMetadata(NamedTuple):
    type: CredentialType


class CredentialState(NamedTuple):
    key: str
    modified_by: str
    modified_date: str
    name: str
    roots: List[str]


class CredentialItem(NamedTuple):
    group_name: str
    id: str
    metadata: CredentialMetadata
    state: CredentialState
