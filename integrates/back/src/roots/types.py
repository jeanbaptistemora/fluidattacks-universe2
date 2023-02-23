from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
)


class Credential(NamedTuple):
    id: str
    name: str
    type: CredentialType | str
    key: str | None = None
    user: str | None = None
    password: str | None = None
    token: str | None = None


class GitRootCloningStatus(NamedTuple):
    message: str
    status: str
    commit: str | None = None
