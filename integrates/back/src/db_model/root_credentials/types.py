from db_model.enums import (
    GitCredentialType,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)


class RootCredentialMetadata(NamedTuple):
    type: GitCredentialType


class RootCredentialState(NamedTuple):
    key: Optional[str]
    modified_by: str
    modified_date: str
    name: str
    roots: List[str]


class RootCredentialItem(NamedTuple):
    group_name: str
    id: str
    metadata: RootCredentialMetadata
    state: RootCredentialState
