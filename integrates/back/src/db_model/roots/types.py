from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class GitRootMetadata(NamedTuple):
    type: str


class GitRootCloning(NamedTuple):
    modified_date: str
    reason: str
    status: str


class GitEnvironmentUrl(NamedTuple):
    url: str


class GitRootState(NamedTuple):
    branch: str
    environment_urls: List[str]
    environment: str
    git_environment_urls: List[GitEnvironmentUrl]
    gitignore: List[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    reason: Optional[str]
    status: str
    url: str


class MachineGitRootExecution(NamedTuple):
    queue_date: Optional[str] = None
    job_id: Optional[str] = None
    finding_code: Optional[str] = None


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    metadata: GitRootMetadata
    state: GitRootState
    machine_execution: Optional[MachineGitRootExecution]


class IPRootMetadata(NamedTuple):
    type: str


class IPRootState(NamedTuple):
    address: str
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    port: str
    reason: Optional[str]
    status: str


class IPRootItem(NamedTuple):
    group_name: str
    id: str
    metadata: IPRootMetadata
    state: IPRootState


class URLRootMetadata(NamedTuple):
    type: str


class URLRootState(NamedTuple):
    host: str
    modified_by: str
    modified_date: str
    nickname: str
    other: Optional[str]
    path: str
    port: str
    protocol: str
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
