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
