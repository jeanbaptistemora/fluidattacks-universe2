# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    FindingNotFound,
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
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from findings.domain import (
    add_comment,
    approve_draft,
    get_oldest_no_treatment,
    get_tracking_vulnerabilities,
    get_treatment_summary,
    mask_finding,
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
from starlette.responses import (
    Response,
)
import time
from typing import (
    Tuple,
)
from vulnerabilities.domain import (
    get_managers_by_size,
    send_treatment_report_mail,
    validate_treatment_change,
)
from vulnerabilities.types import (
    Treatments,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_tracking_vulnerabilities() -> None:
    loaders: Dataloaders = get_new_context()
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    historic_state_loader = loaders.vulnerability_historic_state
    historic_treatment_loader = loaders.vulnerability_historic_treatment

    finding_id = "436992569"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-08-30",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 15,
            "closed": 0,
            "date": "2019-09-12",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 6,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 3,
            "open": 0,
            "closed": 4,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 4,
            "open": 2,
            "closed": 0,
            "date": "2019-09-16",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
    ]
    assert test_data == expected_output

    finding_id = "463461507"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-09-12",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 1,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 1,
            "accepted_undefined": 0,
            "assigned": "integratesuser@gmail.com",
            "justification": "accepted justification",
        },
    ]
    assert test_data == expected_output

    finding_id = "422286126"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2020-01-03",
            "accepted": 0,
            "assigned": "",
            "accepted_undefined": 0,
            "justification": "",
        },
    ]
    assert test_data == expected_output

    finding_id = "463558592"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-01-15",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 0,
            "closed": 1,
            "date": "2019-01-15",
            "accepted": 0,
            "accepted_undefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2019-01-15",
            "accepted": 1,
            "accepted_undefined": 0,
            "assigned": "integratesuser@gmail.com",
            "justification": "This is a treatment justification test",
        },
    ]
    assert test_data == expected_output


@pytest.mark.changes_db
async def test_add_comment() -> None:
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    finding_id = "463461507"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = str(round(time.time() * 1000))
    comment_data = {
        "comment_type": "comment",
        "comment_id": comment_id,
        "content": "Test comment",
        "created": current_time,
        "fullname": "unittesting",
        "modified": current_time,
        "parent": "0",
    }
    assert await add_comment(
        info,
        "unittest@fluidattacks.com",
        comment_data,
        finding_id,
        "unittesting",
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_data["created"] = current_time
    comment_data["modified"] = current_time
    comment_data["parent"] = str(comment_id)
    assert await add_comment(
        info,
        "unittest@fluidattacks.com",
        comment_data,
        finding_id,
        "unittesting",
    )


@pytest.mark.changes_db
async def test_mask_finding() -> None:
    finding_id = "475041524"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    assert await mask_finding(loaders, finding)
    loaders.finding.clear(finding_id)
    with pytest.raises(FindingNotFound):
        await loaders.finding.load(finding_id)


async def test_validate_evidence_records() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    mime_type = "text/csv"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        test_data = await validate_evidence(evidence_id, uploaded_file)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output


async def test_validate_evidence_records_invalid_type() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    mime_type = "image/gif"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        with pytest.raises(InvalidFileType):
            await validate_evidence(evidence_id, uploaded_file)


@freeze_time("2020-10-08")
@pytest.mark.parametrize(
    ["acceptance_date"],
    [
        ["2020-10-06 23:59:59"],  # In the past
        ["2020-12-31 00:00:00"],  # Over org's max_acceptance_days
    ],
)
async def test_validate_past_acceptance_days(acceptance_date: str) -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
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
            severity,
            historic_treatment,
            get_new_context(),
            org_id,
            values_accepted,
        )


async def test_validate_acceptance_severity() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
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
            severity,
            historic_treatment,
            get_new_context(),
            org_id,
            values_accepted,
        )


async def test_validate_number_acceptances() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
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
            severity,
            historic_treatment,
            get_new_context(),
            org_id,
            values_accepted,
        )


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_approve_draft() -> None:
    finding_id = "475041513"
    user_email = "unittest@fluidattacks.com"
    context: Response = await create_dummy_session(user_email)
    loaders: Dataloaders = context.loaders
    historic_state_loader = loaders.vulnerability_historic_state
    historic_treatment_loader = loaders.vulnerability_historic_treatment

    approval_date = await approve_draft(context, finding_id, user_email)
    expected_date = "2019-12-01T00:00:00+00:00"
    assert isinstance(approval_date, str)
    assert approval_date == expected_date

    all_vulns = await loaders.finding_vulnerabilities_all.load(finding_id)
    vuln_ids = [vuln.id for vuln in all_vulns]

    for vuln_id in vuln_ids:
        historic_state_loader.clear(vuln_id)
        historic_state = await historic_state_loader.load(vuln_id)
        for state in historic_state:
            assert state.modified_date == expected_date

        historic_treatment_loader.clear(vuln_id)
        historic_treatment = await historic_treatment_loader.load(vuln_id)
        for treatment in historic_treatment:
            assert treatment.modified_date == expected_date


@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment_findings() -> None:
    group_name = "oneshottest"
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    oldest_findings = await get_oldest_no_treatment(loaders, findings)
    expected_output = {
        "oldest_name": "037. Technical information leak",
        "oldest_age": 256,
    }
    assert expected_output == oldest_findings


@freeze_time("2021-05-27")
async def test_get_treatment_summary() -> None:
    loaders = get_new_context()
    finding_id = "475041513"
    oldest_findings = await get_treatment_summary(loaders, finding_id)
    expected_output = Treatments(
        accepted=0,
        accepted_undefined=0,
        in_progress=0,
        new=1,
    )
    assert expected_output == oldest_findings


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
            "15375781-31f2-4953-ac77-f31134225747",
            False,
        ],
        [
            "vulnmanager@gmail.com",
            "test",
            "15375781-31f2-4953-ac77-f31134225747",
            True,
        ],
    ],
)
async def test_send_treatment_report_mail(
    modified_by: str,
    justification: str,
    vulnerability_id: str,
    is_approved: bool,
) -> None:
    await send_treatment_report_mail(
        loaders=get_new_context(),
        modified_by=modified_by,
        justification=justification,
        vulnerability_id=vulnerability_id,
        is_approved=is_approved,
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


@pytest.mark.asyncio
async def test_get_managers_by_size() -> None:
    group_name = "unittesting"
    email_managers = await get_managers_by_size(group_name, 3)
    expected_len = 3
    assert expected_len == len(email_managers)
    email_managers = await get_managers_by_size(group_name, 2)
    expected_len = 2
    assert expected_len == len(email_managers)
