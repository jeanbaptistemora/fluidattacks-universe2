from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class GitRootMetadata(NamedTuple):
    type: str


class GitRootCloning(NamedTuple):
    modified_date: Optional[str]
    reason: Optional[str]
    status: Optional[str]


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
    queue_date: str
    job_id: str
    finding_code: str


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    metadata: GitRootMetadata
    state: GitRootState
    machine_execution: Optional[List[MachineGitRootExecution]]


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


class MachineFindingResult(NamedTuple):
    open: int
    finding: str


class RootMachineExecutionItem(NamedTuple):
    job_id: str
    created_at: str
    started_at: str
    stopped_at: str
    name: str
    findings_executed: List[MachineFindingResult]
    queue: str
