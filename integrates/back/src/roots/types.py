from typing import (
    List,
    NamedTuple,
    Union,
)


class GitRootCloningStatus(NamedTuple):
    message: str
    status: str


class GitEnvironmentUrl(NamedTuple):
    url: str


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
    last_cloning_status_update: str
    nickname: str
    state: str
    url: str


class IPRoot(NamedTuple):
    address: str
    id: str
    nickname: str
    port: int
    state: str


class URLRoot(NamedTuple):
    host: str
    id: str
    nickname: str
    path: str
    port: int
    protocol: str
    state: str


Root = Union[GitRoot, IPRoot, URLRoot]
