# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
)
from findings.domain import (
    add_comment,
    get_oldest_no_treatment,
    get_tracking_vulnerabilities,
    get_treatment_summary,
    has_access_to_finding,
    mask_finding,
)
from freezegun import (  # type: ignore
    freeze_time,
)
from newutils.datetime import (
    get_as_utc_iso_format,
    get_now,
)
import pytest
import time
from typing import (
    Tuple,
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


async def test_has_access_to_finding() -> None:
    loaders = get_new_context()
    wrong_data = ["unittest@fluidattacks.com", "000000000"]
    right_data = ["unittest@fluidattacks.com", "560175507"]
    with pytest.raises(FindingNotFound):
        await has_access_to_finding(loaders, wrong_data[0], wrong_data[1])
    assert await has_access_to_finding(loaders, right_data[0], right_data[1])


@pytest.mark.changes_db
async def test_add_comment() -> None:
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    finding_id = "463461507"
    current_time = get_as_utc_iso_format(get_now())
    comment_id = str(round(time.time() * 1000))
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.COMMENT,
        id=comment_id,
        content="Test comment",
        creation_date=current_time,
        full_name="unittesting",
        parent_id="0",
        email="unittest@fluidattacks.com",
    )
    await add_comment(
        info,
        "unittest@fluidattacks.com",
        comment_data,
        finding_id,
        "unittesting",
    )
    loaders = get_new_context()
    finding_comments: list[
        FindingComment
    ] = await loaders.finding_comments.load((CommentType.COMMENT, finding_id))
    assert finding_comments[-1].content == "Test comment"
    assert finding_comments[-1].full_name == "unittesting"

    current_time = get_as_utc_iso_format(get_now())
    new_comment_data = comment_data._replace(
        creation_date=current_time, parent_id=str(comment_id)
    )
    await add_comment(
        info,
        "unittest@fluidattacks.com",
        new_comment_data,
        finding_id,
        "unittesting",
    )
    new_loaders = get_new_context()
    new_finding_comments: list[
        FindingComment
    ] = await new_loaders.finding_comments.load(
        (CommentType.COMMENT, finding_id)
    )
    assert new_finding_comments[-1].content == "Test comment"
    assert new_finding_comments[-1].parent_id == str(comment_id)


@pytest.mark.changes_db
async def test_mask_finding() -> None:
    finding_id = "475041524"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    await mask_finding(loaders, finding)
    loaders.finding.clear(finding_id)
    with pytest.raises(FindingNotFound):
        await loaders.finding.load(finding_id)


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
