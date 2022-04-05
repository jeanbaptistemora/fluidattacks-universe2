from db_model.enums import (
    CredentialType,
)
from typing import (
    List,
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


class GitEnvironmentUrl(NamedTuple):
    url: str


class Secret(NamedTuple):
    key: str
    value: str
    descrition: Optional[str] = None


class GitRoot(NamedTuple):
    branch: str
    cloning_status: GitRootCloningStatus
    environment_urls: List[str]
    git_environment_urls: List[GitEnvironmentUrl]
    environment: str
    gitignore: List[str]
    group_name: str
    id: str
    includes_health_check: bool
    last_state_status_update: str
    last_cloning_status_update: str
    nickname: str
    state: str
    url: str
    download_url: Optional[str] = None
    upload_url: Optional[str] = None
    use_vpn: bool = False
    secrets: List[Secret] = []


class IPRoot(NamedTuple):
    address: str
    group_name: str
    id: str
    nickname: str
    port: int
    state: str


class URLRoot(NamedTuple):
    group_name: str
    host: str
    id: str
    nickname: str
    path: str
    port: int
    protocol: str
    state: str


Root = Union[GitRoot, IPRoot, URLRoot]
