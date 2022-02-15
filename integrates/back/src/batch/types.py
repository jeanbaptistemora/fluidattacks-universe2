from batch.enums import (
    JobStatus,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)


class BatchProcessing(NamedTuple):
    key: str
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str
    queue: str


class VulnerabilitiesSummary(NamedTuple):
    open: int
    modified: int


class Job(NamedTuple):
    created_at: Optional[int]
    exit_code: Optional[int]
    exit_reason: Optional[str]
    id: str
    name: str
    queue: str
    started_at: Optional[int]
    stopped_at: Optional[int]
    status: str
    vulnerabilities: Optional[VulnerabilitiesSummary] = None
    root_nickname: Optional[str] = None


class JobContainer(NamedTuple):
    command: List[str]


class JobDescription(NamedTuple):
    id: str
    name: str
    status: JobStatus
    container: JobContainer


class JobPayload(NamedTuple):
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str


class CloneResult(NamedTuple):
    success: bool
    commit: Optional[str] = None
    commit_date: Optional[str] = None
