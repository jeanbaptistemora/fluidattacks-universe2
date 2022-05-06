from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
    Optional,
    Union,
)


class Credential(NamedTuple):
    id: str
    name: str
    type: Union[CredentialType, str]


class GitRootCloningStatus(NamedTuple):
    message: str
    status: str
    commit: Optional[str] = None
