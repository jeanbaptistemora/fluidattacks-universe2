from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class GitRootMetadata(NamedTuple):
    branch: str
    type: str
    url: str


class GitRootCloning(NamedTuple):
    modified_date: str
    reason: str
    status: str


class GitEnvironmentUrl(NamedTuple):
    url: str


class GitRootState(NamedTuple):
    environment: str
    environment_urls: List[str]
    git_environment_urls: List[GitEnvironmentUrl]
    gitignore: List[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    reason: Optional[str]
    status: str


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    metadata: GitRootMetadata
    state: GitRootState


class IPRootMetadata(NamedTuple):
    address: str
    type: str
    port: str


class IPRootState(NamedTuple):
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    reason: Optional[str]
    status: str


class IPRootItem(NamedTuple):
    group_name: str
    id: str
    metadata: IPRootMetadata
    state: IPRootState


class URLRootMetadata(NamedTuple):
    host: str
    path: str
    port: str
    protocol: str
    type: str


class URLRootState(NamedTuple):
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    reason: Optional[str]
    status: str


class URLRootItem(NamedTuple):
    group_name: str
    id: str
    metadata: URLRootMetadata
    state: URLRootState


RootItem = Union[GitRootItem, IPRootItem, URLRootItem]


class RootState(NamedTuple):
    modified_by: str
    modified_date: str
    other: Optional[str]
    reason: Optional[str]
    status: str
