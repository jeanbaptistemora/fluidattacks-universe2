# Standard
from typing import List, NamedTuple, Union


class GitRootCloningStatus(NamedTuple):
    message: str
    status: str


class GitRoot(NamedTuple):
    branch: str
    cloning_status: GitRootCloningStatus
    environment_urls: List[str]
    environment: str
    gitignore: List[str]
    id: str
    includes_health_check: bool
    last_status_update: str
    nickname: str
    state: str
    url: str


class IPRoot(NamedTuple):
    address: str
    id: str
    port: int


class URLRoot(NamedTuple):
    host: str
    id: str
    path: str
    port: int
    protocol: str


Root = Union[GitRoot, IPRoot, URLRoot]
