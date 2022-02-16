from db_model.enums import (
    GitCloningStatus,
)
from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class RootUnreliableIndicators(NamedTuple):
    unreliable_last_status_update: str = ""


class RootUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_last_status_update: Optional[str] = None


class GitRootCloning(NamedTuple):
    modified_date: str
    reason: str
    status: GitCloningStatus
    commit: Optional[str] = None
    commit_date: Optional[str] = None


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


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    organization_name: str
    state: GitRootState
    type: str
    unreliable_indicators: RootUnreliableIndicators = (
        RootUnreliableIndicators()
    )


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
    organization_name: str
    state: IPRootState
    type: str
    unreliable_indicators: RootUnreliableIndicators = (
        RootUnreliableIndicators()
    )


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
    organization_name: str
    state: URLRootState
    type: str
    unreliable_indicators: RootUnreliableIndicators = (
        RootUnreliableIndicators()
    )


RootItem = Union[GitRootItem, IPRootItem, URLRootItem]


class RootState(NamedTuple):
    modified_by: str
    modified_date: str
    other: Optional[str]
    reason: Optional[str]
    status: str


class MachineFindingResult(NamedTuple):
    open: int
    modified: int
    finding: str


class RootMachineExecutionItem(NamedTuple):
    job_id: str
    created_at: str
    started_at: Optional[str]
    stopped_at: Optional[str]
    name: str
    findings_executed: List[MachineFindingResult]
    queue: str
    root_id: str
    commit: Optional[str] = None


class LastMachineExecutions(NamedTuple):
    complete: Optional[RootMachineExecutionItem]
    specific: Optional[RootMachineExecutionItem]
