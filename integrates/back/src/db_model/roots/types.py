from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from typing import (
    List,
    Literal,
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


class Secret(NamedTuple):
    key: str
    value: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


class GitEnvironmentUrl(NamedTuple):
    url: str
    id: str
    secrets: list[Secret] = []
    created_at: Optional[datetime] = None
    group_name: Optional[str] = None


class GitRootState(NamedTuple):
    branch: str
    environment: str
    includes_health_check: bool
    modified_by: str
    modified_date: str
    nickname: str
    status: RootStatus
    url: str
    environment_urls: List[str] = []
    download_url: Optional[str] = None
    git_environment_urls: List[GitEnvironmentUrl] = []
    gitignore: List[str] = []
    other: Optional[str] = None
    reason: Optional[str] = None
    secrets: List[Secret] = []
    upload_url: Optional[str] = None
    use_vpn: bool = False


class GitRoot(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    organization_name: str
    state: GitRootState
    type: Literal[RootType.GIT]
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
    status: RootStatus


class IPRoot(NamedTuple):
    group_name: str
    id: str
    organization_name: str
    state: IPRootState
    type: Literal[RootType.IP]
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
    status: RootStatus


class URLRoot(NamedTuple):
    group_name: str
    id: str
    organization_name: str
    state: URLRootState
    type: Literal[RootType.URL]
    unreliable_indicators: RootUnreliableIndicators = (
        RootUnreliableIndicators()
    )


Root = Union[GitRoot, IPRoot, URLRoot]


class RootState(NamedTuple):
    modified_by: str
    modified_date: str
    nickname: Optional[str]
    other: Optional[str]
    reason: Optional[str]
    status: RootStatus


class MachineFindingResult(NamedTuple):
    open: int
    modified: int
    finding: str


class RootMachineExecution(NamedTuple):
    job_id: str
    name: str
    findings_executed: List[MachineFindingResult]
    queue: str
    root_id: str
    created_at: str
    started_at: Optional[str]
    stopped_at: Optional[str] = None
    commit: Optional[str] = None
    success: bool = True
    status: Optional[str] = None


class LastMachineExecutions(NamedTuple):
    complete: Optional[RootMachineExecution]
    specific: Optional[RootMachineExecution]
