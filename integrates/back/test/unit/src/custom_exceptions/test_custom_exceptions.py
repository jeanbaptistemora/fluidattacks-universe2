from custom_exceptions import (
    EventNotFound,
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidFileType,
    InvalidNumberAcceptances,
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from findings.domain import (
    validate_evidence,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from vulnerabilities.domain import (
    send_treatment_report_mail,
    validate_treatment_change,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_exception_event_not_found() -> None:
    loaders: Dataloaders = get_new_context()
    with pytest.raises(EventNotFound):
        await loaders.event.load("000001111")


@freeze_time("2020-10-08")
@pytest.mark.parametrize(
    ["acceptance_date"],
    [
        ["2020-10-06 23:59:59"],  # In the past
        ["2020-12-31 00:00:00"],  # Over org's max_acceptance_days
    ],
)
async def test_validate_past_acceptance_days(acceptance_date: str) -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 5
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidAcceptanceDays):
        assert await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


async def test_validate_acceptance_severity() -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 8.5
    acceptance_date = (datetime.now() + timedelta(days=10)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidAcceptanceSeverity):
        assert await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


async def test_validate_evidence_records_invalid_type() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/test-anim.gif")
    mime_type = "image/gif"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        with pytest.raises(InvalidFileType):
            await validate_evidence(evidence_id, uploaded_file)


async def test_validate_number_acceptances() -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-01-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.ACCEPTED,
            accepted_until="2020-02-01T17:00:00+00:00",
            justification="Justification to accept the finding",
            modified_by="unittest@fluidattacks.com",
        ),
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 5
    acceptance_date = (datetime.now() + timedelta(days=10)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidNumberAcceptances):
        assert await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "modified_by",
        "justification",
        "vulnerability_id",
        "is_approved",
    ],
    [
        [
            "vulnmanager@gmail.com",
            "test",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            False,
        ],
    ],
)
async def test_send_treatment_report_mail_fail(
    modified_by: str,
    justification: str,
    vulnerability_id: str,
    is_approved: bool,
) -> None:
    with pytest.raises(VulnNotFound):
        await send_treatment_report_mail(
            loaders=get_new_context(),
            modified_by=modified_by,
            justification=justification,
            vulnerability_id=vulnerability_id,
            is_approved=is_approved,
        )
