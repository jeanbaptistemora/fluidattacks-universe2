from batch import (
    dal as batch_dal,
    domain as batch_domain,
)
from batch.enums import (
    JobStatus,
)
from batch.types import (
    BatchProcessing,
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
    additional_info = "aditional-test"
    job_description = BatchProcessing(
        key="42343434",
        action_name=action_name.lower(),
        entity=entity.lower(),
        subject=subject.lower(),
        time=time,
        additional_info=additional_info,
        queue="spot_soon",
    )
    job_payload = batch_domain.format_job_payload(job_description)
    assert job_payload == JobPayload(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
    )
