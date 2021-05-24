import os
import pytest
import time
from datetime import (
    datetime,
    timedelta,
)

from freezegun import freeze_time
from graphql.type import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from back.tests.unit.utils import create_dummy_session
from custom_exceptions import (
    InvalidAcceptanceSeverity,
    InvalidFileType,
    InvalidNumberAcceptations,
)
from dataloaders import get_new_context
from findings import dal as findings_dal
from findings.domain import (
    add_comment,
    approve_draft,
    get_oldest_open_findings,
    get_total_reattacks_stats,
    get_total_treatment_date,
    get_tracking_vulnerabilities,
    list_drafts,
    list_findings,
    mask_finding,
    validate_evidence,
)
from mailer import common as mailer_utils
from newutils import datetime as datetime_utils
from vulnerabilities.domain import (
    list_vulnerabilities_async,
    validate_treatment_change,
)


pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_comment_recipients():
    project_name = "unittesting"
    comment_type = "comment"

    test_data = await mailer_utils.get_comment_recipients(
        project_name, comment_type
    )
    assert isinstance(test_data, list)
    assert isinstance(test_data[0], str)


async def test_get_tracking_vulnerabilities():
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
async def test_add_comment():
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
    finding_id = "463461507"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = int(round(time.time() * 1000))
    comment_data = {
        "comment_type": "comment",
        "user_id": comment_id,
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
async def test_mask_finding():
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


async def test_validate_evidence_records():
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


async def test_validate_evidence_records_invalid_type():
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    mime_type = "image/gif"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        with pytest.raises(InvalidFileType) as context:
            await validate_evidence(evidence_id, uploaded_file)


async def test_validate_acceptance_severity():
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


async def test_validate_number_acceptations():
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


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_approve_draft():
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
    assert test_success, test_date == expected_output
    all_vulns = await list_vulnerabilities_async(
        [finding_id],
        should_list_deleted=True,
        include_requested_zero_risk=True,
        include_confirmed_zero_risk=True,
    )
    for vuln in all_vulns:
        for state_info in vuln["historic_state"]:
            assert state_info["date"] == release_date


async def test_list_findings() -> None:
    context = get_new_context()
    project_name = "unittesting"
    test_data = await list_findings(context, [project_name])
    expected_output = [
        "988493279",
        "422286126",
        "436992569",
        "463461507",
        "463558592",
        "457497316",
    ]
    assert expected_output == test_data[0]


async def test_list_drafts() -> None:
    project_name = "unittesting"
    test_data = await list_drafts([project_name])
    expected_output = ["560175507"]
    assert expected_output == test_data[0]


async def test_list_drafts_deleted() -> None:
    projects_name = ["continuoustesting"]
    test_data = await list_drafts(projects_name)
    expected_output = ["818828206", "836530833", "475041524"]
    assert sorted(expected_output) == sorted(test_data[0])
    test_data = await list_drafts(projects_name, include_deleted=True)
    expected_output = ["818828206", "836530833", "475041524", "991607942"]
    assert sorted(expected_output) == sorted(test_data[0])


@freeze_time("2019-01-26")
async def test_get_oldest_open_findings():
    project_name = "unittesting"
    oldest_requested = 1
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(project_name)
    oldest_findings = await get_oldest_open_findings(
        context, findings, oldest_requested
    )
    expected_output = [
        {
            "finding_name": "F007. Cross site request forgery",
            "finding_age": 10,
        }
    ]
    assert expected_output == oldest_findings


@freeze_time("2018-12-27")
async def test_get_total_reattacks_stats():
    project_name = "unittesting"
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(project_name)
    treatment_stats = await get_total_treatment_date(
        context, findings, last_day
    )
    expected_output = {
        "accepted": 3,
        "accepted_undefined_submitted": 1,
        "accepted_undefined_approved": 1,
    }
    assert expected_output == treatment_stats


@freeze_time("2018-12-27")
async def test_get_total_reattacks_stats():
    project_name = "unittesting"
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(project_name)
    reattacks_stats = await get_total_reattacks_stats(
        context, findings, last_day
    )
    expected_output = {
        "reattacks_requested": 2,
        "reattacks_executed": 1,
        "pending_attacks": 1,
        "reattack_effectiveness": 0,
    }
    assert expected_output == reattacks_stats
