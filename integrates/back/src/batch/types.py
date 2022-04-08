from batch.enums import (
    JobStatus,
)
from custom_exceptions import (
    CustomBaseException,
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
    batch_job_id: Optional[str] = None
    running: bool = False


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
    message: Optional[str] = None


class PutActionResult(NamedTuple):
    success: bool
    batch_job_id: Optional[str] = None
    dynamo_pk: Optional[str] = None


class AttributesNoOverridden(CustomBaseException):
    """Exception to control attributes that can be overridden."""

    def __init__(self, *attributes: str) -> None:
        """Constructor"""
        msg = (
            "Exception - the following attributes "
            f"can not be override {','.join(attributes)}"
        )
        super().__init__(msg)
