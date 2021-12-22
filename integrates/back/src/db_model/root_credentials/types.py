from typing import (
    List,
    NamedTuple,
    Optional,
)


class RootCredentialMetadata(NamedTuple):
    type: str


class RootCredentialState(NamedTuple):
    key: Optional[str]
    key_username: Optional[str]
    modified_by: str
    modified_date: str
    name: str
    roots: List[str]
    status: str


class RootCredentialItem(NamedTuple):
    group_name: str
    id: str
    metadata: RootCredentialMetadata
    state: RootCredentialState
