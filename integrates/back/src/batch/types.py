from batch.enums import (
    JobStatus,
)
from custom_exceptions import (
    CustomBaseException,
)
from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class BatchProcessing(NamedTuple):
    key: str
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str
    queue: str
    batch_job_id: str | None = None
    retries: int = 0
    running: bool = False


class Job(NamedTuple):
    created_at: int | None
    exit_code: int | None
    exit_reason: str | None
    id: str
    name: str
    queue: str
    started_at: int | None
    stopped_at: int | None
    status: str
    root_nickname: str | None = None


class JobContainer(NamedTuple):
    command: list[str]


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
    commit: str | None = None
    commit_date: datetime | None = None
    message: str | None = None


class PutActionResult(NamedTuple):
    success: bool
    batch_job_id: str | None = None
    dynamo_pk: str | None = None


class AttributesNoOverridden(CustomBaseException):
    """Exception to control attributes that can be overridden."""

    def __init__(self, *attributes: str) -> None:
        """Constructor"""
        msg = (
            "Exception - the following attributes "
            f"can not be override {','.join(attributes)}"
        )
        super().__init__(msg)
