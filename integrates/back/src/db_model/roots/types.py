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
from db_model.types import (
    CodeLanguage,
)
from enum import (
    Enum,
)
from typing import (
    Literal,
    NamedTuple,
)


class RootUnreliableIndicators(NamedTuple):
    unreliable_code_languages: list[CodeLanguage] = []
    unreliable_last_status_update: datetime | None = None


class RootUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_code_languages: list[CodeLanguage] | None = None
    unreliable_last_status_update: datetime | None = None


class GitRootCloning(NamedTuple):
    modified_date: datetime
    reason: str
    status: GitCloningStatus
    commit: str | None = None
    commit_date: datetime | None = None


class Secret(NamedTuple):
    key: str
    value: str
    description: str | None = None
    created_at: datetime | None = None


class RootEnvironmentUrlType(str, Enum):
    URL: str = "URL"
    CLOUD: str = "CLOUD"
    DATABASE: str = "DATABASE"
    APK: str = "APK"


class RootEnvironmentCloud(str, Enum):
    AWS: str = "AWS"
    GCP: str = "GCP"
    AZURE: str = "AZURE"
    KUBERNETES: str = "KUBERNETES"


class RootEnvironmentUrl(NamedTuple):
    url: str
    id: str
    secrets: list[Secret] = []
    created_at: datetime | None = None
    created_by: str | None = None
    group_name: str | None = None
    url_type: RootEnvironmentUrlType = RootEnvironmentUrlType.URL
    cloud_name: RootEnvironmentCloud | None = None


class GitRootState(NamedTuple):
    branch: str
    environment: str
    includes_health_check: bool
    modified_by: str
    modified_date: datetime
    nickname: str
    status: RootStatus
    url: str
    credential_id: str | None = None
    gitignore: list[str] = []
    other: str | None = None
    reason: str | None = None
    use_vpn: bool = False


class GitRoot(NamedTuple):
    cloning: GitRootCloning
    created_by: str
    created_date: datetime
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
    modified_date: datetime
    nickname: str
    other: str | None
    reason: str | None
    status: RootStatus


class IPRoot(NamedTuple):
    created_by: str
    created_date: datetime
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
    modified_date: datetime
    nickname: str
    other: str | None
    path: str
    port: str
    protocol: str
    reason: str | None
    status: RootStatus
    query: str | None = None


class URLRoot(NamedTuple):
    created_by: str
    created_date: datetime
    group_name: str
    id: str
    organization_name: str
    state: URLRootState
    type: Literal[RootType.URL]
    unreliable_indicators: RootUnreliableIndicators = (
        RootUnreliableIndicators()
    )


Root = GitRoot | IPRoot | URLRoot


class RootState(NamedTuple):
    modified_by: str
    modified_date: datetime
    nickname: str | None
    other: str | None
    reason: str | None
    status: RootStatus


class MachineFindingResult(NamedTuple):
    open: int
    modified: int
    finding: str


class RootMachineExecution(NamedTuple):
    job_id: str
    name: str
    findings_executed: list[MachineFindingResult]
    queue: str
    root_id: str
    created_at: datetime
    started_at: datetime | None = None
    stopped_at: datetime | None = None
    commit: str | None = None
    success: bool = True
    status: str | None = None


class RootRequest(NamedTuple):
    group_name: str
    root_id: str
