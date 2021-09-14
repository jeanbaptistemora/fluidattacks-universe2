from back.tests.unit import (
    MIGRATION,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from custom_exceptions import (
    InvalidAcceptanceSeverity,
    InvalidFileType,
    InvalidNumberAcceptations,
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
from findings import (
    dal as findings_dal,
)
from findings.domain import (
    add_comment,
    approve_draft,
    approve_draft_new,
    get_oldest_no_treatment,
    get_oldest_no_treatment_new,
    get_tracking_vulnerabilities,
    list_drafts,
    list_findings,
    list_findings_new,
    mask_finding,
    mask_finding_new,
    validate_evidence,
)
from freezegun import (
    freeze_time,
)
from graphql.type import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
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
    list_vulnerabilities_async,
    validate_treatment_change,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_tracking_vulnerabilities() -> None:
    finding_id = "436992569"
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-08-30",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 15,
            "closed": 0,
            "date": "2019-09-12",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 6,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 3,
            "open": 0,
            "closed": 4,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 4,
            "open": 2,
            "closed": 0,
            "date": "2019-09-16",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
    ]
    assert test_data == expected_output

    finding_id = "463461507"
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-09-12",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 1,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2019-09-13",
            "accepted": 1,
            "accepted_undefined": 0,
            "manager": "integratesuser@gmail.com",
            "justification": "accepted justification",
        },
    ]
    assert test_data == expected_output

    finding_id = "422286126"
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2020-01-03",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
    ]
    assert test_data == expected_output

    finding_id = "463558592"
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2019-01-15",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 0,
            "closed": 1,
            "date": "2019-01-15",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2019-01-15",
            "accepted": 1,
            "accepted_undefined": 0,
            "manager": "integratesuser@gmail.com",
            "justification": "This is a treatment justification test",
        },
    ]
    assert test_data == expected_output


@pytest.mark.changes_db
async def test_add_comment() -> None:
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
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


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_mask_finding() -> None:
    finding_id = "475041524"
    context = get_new_context()
    test_data = await mask_finding(context, finding_id)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

    finding = await findings_dal.get_finding(finding_id)
    assert finding.get("vulnerability", "") == "Masked"
    assert finding.get("files", [{}])[-1].get("file_url", "") == "Masked"
    assert finding.get("effect_solution", "") == "Masked"
    assert finding.get("affected_systems", "") == "Masked"


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_mask_finding_new() -> None:
    finding_id = "475041524"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding_new.load(finding_id)
    success = await mask_finding_new(loaders, finding)
    assert isinstance(success, bool)
    assert success == True

    masked_msg = "Masked"
    loaders.finding_new.clear(finding_id)
    masked_finding: Finding = await loaders.finding_new.load(finding_id)
    assert masked_finding.affected_systems == masked_msg
    assert masked_finding.attack_vector_description == masked_msg
    assert masked_finding.compromised_attributes == masked_msg
    assert masked_finding.description == masked_msg
    assert masked_finding.recommendation == masked_msg
    assert masked_finding.threat == masked_msg
    assert masked_finding.evidences.evidence1.description == masked_msg
    assert masked_finding.evidences.evidence1.url == masked_msg
    assert masked_finding.evidences.evidence2.description == masked_msg
    assert masked_finding.evidences.evidence2.url == masked_msg


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


async def test_validate_acceptance_severity() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    info_to_check = {
        "historic_treatment": [
            {
                "date": "2020-02-01 12:00:00",
                "treatment": "NEW",
                "user": "unittest@fluidattacks.com",
            }
        ],
        "severity": 8.5,
    }
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
            info_to_check,
            get_new_context(),
            org_id,
            values_accepted,
        )


async def test_validate_number_acceptations() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    info_to_check = {
        "historic_treatment": [
            {
                "acceptance_date": "2020-02-01 12:00:00",
                "date": "2020-01-01 12:00:00",
                "justification": "Justification to accept the finding",
                "treatment": "ACCEPTED",
                "user": "unittest@fluidattacks.com",
            },
            {
                "date": "2020-02-01 12:00:00",
                "treatment": "NEW",
                "user": "unittest@fluidattacks.com",
            },
        ],
        "severity": 5,
    }
    acceptance_date = (datetime.now() + timedelta(days=10)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidNumberAcceptations):
        assert await validate_treatment_change(
            info_to_check,
            get_new_context(),
            org_id,
            values_accepted,
        )


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_approve_draft() -> None:
    finding_id = "475041513"
    reviewer_email = "unittest@fluidattacks.com"
    context = await create_dummy_session(reviewer_email)
    test_success, test_date = await approve_draft(
        context, finding_id, reviewer_email
    )
    release_date = "2019-11-30 19:00:00"
    expected_output = True, release_date
    assert isinstance(test_success, bool)
    assert isinstance(test_date, str)
    assert test_success, test_date == expected_output  # type: ignore
    all_vulns = await list_vulnerabilities_async(
        [finding_id],
        should_list_deleted=True,
        include_requested_zero_risk=True,
        include_confirmed_zero_risk=True,
    )
    for vuln in all_vulns:
        for state_info in vuln["historic_state"]:
            assert state_info["date"] == release_date
        for treatment_info in vuln["historic_treatment"]:
            assert treatment_info["date"] == release_date


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_approve_draft_new() -> None:
    finding_id = "475041513"
    user_email = "unittest@fluidattacks.com"
    context: Response = await create_dummy_session(user_email)
    approval_date = await approve_draft_new(context, finding_id, user_email)

    expected_date = "2019-11-30 19:00:00"
    assert isinstance(approval_date, str)
    assert approval_date == datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_from_str(expected_date)
    )
    all_vulns = await list_vulnerabilities_async(
        [finding_id],
        should_list_deleted=True,
        include_requested_zero_risk=True,
        include_confirmed_zero_risk=True,
    )
    for vuln in all_vulns:
        for state_info in vuln["historic_state"]:
            assert state_info["date"] == expected_date
        for treatment_info in vuln["historic_treatment"]:
            assert treatment_info["date"] == expected_date


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_list_findings() -> None:
    context = get_new_context()
    group_name = "unittesting"
    test_data = await list_findings(context, [group_name])
    expected_output = [
        "988493279",
        "422286126",
        "436992569",
        "463461507",
        "463558592",
        "457497316",
    ]
    assert expected_output == test_data[0]


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
async def test_list_findings_new() -> None:
    context = get_new_context()
    group_name = "unittesting"
    test_data = await list_findings_new(context, [group_name])
    expected_output = [
        "988493279",
        "422286126",
        "436992569",
        "463461507",
        "463558592",
        "457497316",
    ]
    assert sorted(expected_output) == sorted(test_data[0])


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_list_drafts() -> None:
    group_name = "unittesting"
    test_data = await list_drafts([group_name])
    expected_output = ["560175507"]
    assert expected_output == test_data[0]


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_list_drafts_deleted() -> None:
    groups_name = ["continuoustesting"]
    test_data = await list_drafts(groups_name)
    expected_output = ["836530833", "475041524"]
    assert sorted(expected_output) == sorted(test_data[0])
    test_data = await list_drafts(groups_name, include_deleted=True)
    expected_output = ["836530833", "475041524", "991607942"]
    assert sorted(expected_output) == sorted(test_data[0])


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment_findings() -> None:
    group_name = "oneshottest"
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group_name)
    oldest_findings = await get_oldest_no_treatment(context, findings)
    expected_output = {
        "oldest_name": "037. Technical information leak",
        "oldest_age": 256,
    }
    assert expected_output == oldest_findings


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment_findings_new() -> None:
    group_name = "oneshottest"
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings_new.load(
        group_name
    )
    oldest_findings = await get_oldest_no_treatment_new(loaders, findings)
    expected_output = {
        "oldest_name": "037. Technical information leak",
        "oldest_age": 256,
    }
    assert expected_output == oldest_findings
