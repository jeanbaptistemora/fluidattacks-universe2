from batch import (
    dal as batch_dal,
    domain as batch_domain,
)
from batch.enums import (
    JobStatus,
)
from batch.types import (
    JobContainer,
    JobDescription,
    JobPayload,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_format_job_payload() -> None:
    action_name = "job-name"
    subject = "test@test.com"
    entity = "group-name"
    time = "0918403984"
    aditional_info = "aditional-test"
    command = batch_dal.format_command(
        action_name=action_name,
        subject=subject,
        entity=entity,
        time=time,
        additional_info=aditional_info,
    )
    job_description = JobDescription(
        id="42343434",
        name=action_name,
        status=JobStatus.RUNNABLE,
        container=JobContainer(command=command),
    )
    job_payload = batch_domain.format_job_payload(job_description)
    assert job_payload == JobPayload(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=aditional_info,
    )
