import pytest
import time
from decimal import Decimal
from datetime import datetime

from aioextensions import collect
from freezegun import freeze_time
from graphql.type import GraphQLResolveInfo
from pytz import timezone

from back.tests.unit.utils import create_dummy_session
from custom_exceptions import (
    InvalidGroupServicesConfig,
    RepeatedValues,
)
from dataloaders import get_new_context
from events.domain import list_group_events
from findings import dal as findings_dal
from findings.domain import (
    get_last_closing_vuln_info,
    get_max_open_severity,
    get_pending_closing_check,
    get_pending_verification_findings,
    get_total_treatment,
)
from group_access.domain import (
    get_closers,
    get_managers,
    get_group_users,
    remove_access,
)
from group_comments.domain import (
    add_comment,
    get_total_comments_date,
    list_comments,
)
from groups.domain import (
    create_group,
    edit,
    get_active_groups,
    get_alive_group_names,
    get_closed_vulnerabilities,
    get_description,
    get_group_digest_stats,
    get_mean_remediate,
    get_mean_remediate_non_treated,
    get_mean_remediate_severity,
    get_open_finding,
    get_open_vulnerabilities,
    is_alive,
    validate_group_services_config,
    validate_group_tags,
)
from names import domain as names_domain
from newutils import datetime as datetime_utils
from newutils.vulnerabilities import (
    get_last_closing_date,
    get_open_vulnerability_date,
    is_vulnerability_closed,
)
from settings import TIME_ZONE
from vulnerabilities import dal as vulns_dal


pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_group_services_config():
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, True, True, False, False)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, False, False, True, True)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, True, True, True, False)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, False, True, True, True)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(False, False, False, True, True)


@pytest.mark.changes_db
async def test_remove_access():
    assert await remove_access("unittest", "unittesting")
    assert not await remove_access("", "")


async def test_validate_tags():
    assert await validate_group_tags(
        "unittesting", ["testtag", "this-is-ok", "th15-4l50"]
    )
    assert await validate_group_tags(
        "unittesting", ["this-tag-is-valid", "but this is not"]
    ) == ["this-tag-is-valid"]
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags(
            "unittesting", ["same-name", "same-name", "another-one"]
        )
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags("unittesting", ["test-projects"])


async def test_is_alive():
    assert await is_alive("unittesting")
    assert not await is_alive("unexisting_project")


async def test_get_pending_closing_checks():
    context = get_new_context()
    test_data = await get_pending_closing_check(context, "unittesting")
    expected_output = 1
    assert test_data == expected_output


async def test_get_last_closing_vuln():
    findings_to_get = ["463558592", "422286126"]
    context = get_new_context()
    findings = await collect(
        findings_dal.get_finding(finding_id) for finding_id in findings_to_get
    )
    test_data = await get_last_closing_vuln_info(context, findings)
    tzn = timezone(TIME_ZONE)
    actual_date = datetime.now(tz=tzn).date()
    initial_date = datetime(2019, 1, 15).date()
    assert test_data[0] == (actual_date - initial_date).days
    assert test_data[1]["UUID"] == "242f848c-148a-4028-8e36-c7d995502590"
    assert test_data[1]["finding_id"] == "463558592"


async def test_get_last_closing_date():
    closed_vulnerability = {
        "specific": "phone",
        "finding_id": "422286126",
        "UUID": "80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        "historic_state": [
            {"date": "2018-09-28 10:32:58", "state": "open"},
            {"date": "2019-01-08 16:01:26", "state": "closed"},
        ],
        "vuln_type": "inputs",
        "where": "https://example.com",
        "analyst": "testanalyst@test.com",
    }

    open_vulnerability = await vulns_dal.get(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )

    test_data = get_last_closing_date(closed_vulnerability)
    closing_date = datetime(2019, 1, 8).date()
    assert test_data == closing_date

    test_data = get_last_closing_date(open_vulnerability[0])
    assert test_data is None


async def test_is_vulnerability_closed():
    closed_vulnerability = {
        "specific": "phone",
        "finding_id": "422286126",
        "UUID": "80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        "historic_state": [
            {"date": "2018-09-28 10:32:58", "state": "open"},
            {"date": "2019-01-08 16:01:26", "state": "closed"},
        ],
        "vuln_type": "inputs",
        "where": "https://example.com",
        "analyst": "testanalyst@test.com",
    }

    open_vulnerability = await vulns_dal.get(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )

    assert is_vulnerability_closed(closed_vulnerability)
    assert not is_vulnerability_closed(open_vulnerability[0])


async def test_get_max_open_severity():
    findings_to_get = ["463558592", "422286126"]
    findings = await collect(
        findings_dal.get_finding(finding_id) for finding_id in findings_to_get
    )
    test_data = await get_max_open_severity(get_new_context(), findings)
    assert test_data[0] == Decimal(4.3).quantize(Decimal("0.1"))
    assert test_data[1]["finding_id"] == "463558592"


async def test_get_open_vulnerabilities():
    project_name = "unittesting"
    expected_output = 29
    open_vulns = await get_open_vulnerabilities(
        get_new_context(), project_name
    )
    assert open_vulns == expected_output


async def test_get_closed_vulnerabilities():
    project_name = "unittesting"
    expected_output = 7
    closed_vulns = await get_closed_vulnerabilities(
        get_new_context(), project_name
    )
    assert closed_vulns == expected_output


async def test_get_open_finding():
    project_name = "unittesting"
    expected_output = 5
    open_findings = await get_open_finding(get_new_context(), project_name)
    assert open_findings == expected_output


async def test_get_open_vulnerability_date():
    closed_vulnerability = {
        "specific": "phone",
        "finding_id": "422286126",
        "UUID": "80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        "historic_state": [{"date": "2019-01-08 16:01:26", "state": "closed"}],
        "vuln_type": "inputs",
        "where": "https://example.com",
        "analyst": "testanalyst@test.com",
    }

    open_vulnerability = await vulns_dal.get(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )

    test_data = get_open_vulnerability_date(open_vulnerability[0])
    expected_output = datetime(2020, 9, 9).date()
    assert test_data == expected_output

    test_data = get_open_vulnerability_date(closed_vulnerability)
    assert test_data is None


@freeze_time("2020-12-01")
async def test_get_mean_remediate():
    context = get_new_context()
    group_name = "unittesting"
    assert await get_mean_remediate(context, group_name) == Decimal("383.0")
    assert await get_mean_remediate_non_treated(group_name) == Decimal("385.0")

    min_date = datetime_utils.get_now_minus_delta(days=30).date()
    assert await get_mean_remediate(context, group_name, min_date) == Decimal(
        "0.0"
    )
    assert await get_mean_remediate_non_treated(
        group_name, min_date
    ) == Decimal("0.0")

    min_date = datetime_utils.get_now_minus_delta(days=90).date()
    assert await get_mean_remediate(context, group_name, min_date) == Decimal(
        "82.0"
    )
    assert await get_mean_remediate_non_treated(
        group_name, min_date
    ) == Decimal("0.0")


async def test_get_total_treatment():
    context = get_new_context()
    findings_to_get = ["463558592", "422286126"]
    findings = await collect(
        findings_dal.get_finding(finding_id) for finding_id in findings_to_get
    )
    test_data = await get_total_treatment(context, findings)
    expected_output = {
        "inProgress": 1,
        "accepted": 1,
        "acceptedUndefined": 0,
        "undefined": 0,
    }
    assert test_data == expected_output


async def test_list_comments():
    project_name = "unittesting"
    test_data = await list_comments(project_name, "admin")
    expected_output = {
        "content": "Now we can post comments on projects",
        "parent": 0,
        "created": "2018/12/27 16:30:28",
        "id": 1545946228675,
        "fullname": "Hacker at Fluid Attacks",
        "email": "unittest@fluidattacks.com",
        "modified": "2018/12/27 16:30:28",
    }
    assert test_data[0] == expected_output


@pytest.mark.changes_db
async def test_add_comment():
    project_name = "unittesting"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = int(round(time.time() * 1000))
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
    comment_data = {
        "user_id": comment_id,
        "content": "Test comment",
        "created": current_time,
        "fullname": "unittesting",
        "modified": current_time,
        "parent": "0",
    }
    assert await add_comment(
        info, project_name, "unittest@fluidattacks.com", comment_data
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_data["created"] = current_time
    comment_data["modified"] = current_time
    comment_data["parent"] = str(comment_id)
    assert await add_comment(
        info, project_name, "unittest@fluidattacks.com", comment_data
    )


async def test_get_active_groups():
    test_data = await get_active_groups()
    assert test_data is not None


async def test_get_alive_group_names():
    test_data = await get_alive_group_names()
    expected_output = [
        "asgard",
        "barranquilla",
        "continuoustesting",
        "deletegroup",
        "deleteimamura",
        "gotham",
        "lubbock",
        "metropolis",
        "monteria",
        "oneshottest",
        "setpendingdeletion",
        "suspendedtest",
        "unittesting",
    ]

    assert sorted(test_data) == sorted(expected_output)


async def test_list_events():
    project_name = "unittesting"
    expected_output = [
        "540462628",
        "538745942",
        "463578352",
        "484763304",
        "418900971",
    ]
    assert expected_output == await list_group_events(project_name)


async def test_get_managers():
    project_name = "unittesting"
    expected_output = [
        "integratesuser@gmail.com",
        "continuoushacking@gmail.com",
        "continuoushack2@gmail.com",
    ]
    assert expected_output == await get_managers(project_name)


async def test_get_description():
    project_name = "unittesting"
    expected_output = "Integrates unit test project"
    assert expected_output == await get_description(project_name)


async def test_get_users():
    project_name = "unittesting"
    expected_output = [
        "integratescloser@fluidattacks.com",
        "integratesserviceforces@gmail.com",
        "integratesmanager@gmail.com",
        "unittest@fluidattacks.com",
        "unittest2@fluidattacks.com",
        "integratesexecutive@gmail.com",
        "integratescustomer@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratescustomer@gmail.com",
        "integratesuser@gmail.com",
        "integratesanalyst@fluidattacks.com",
        "continuoushacking@gmail.com",
        "integratesmanager@fluidattacks.com",
        "continuoushack2@gmail.com",
        "integratesreviewer@fluidattacks.com",
    ]
    assert expected_output == await get_group_users(project_name)


async def test_get_closers():
    closers = await get_closers("oneshottest")
    assert closers == ["integratesanalyst@fluidattacks.com"]


@freeze_time("2020-04-12")
async def test_get_mean_remediate_severity():
    context = get_new_context()
    project_name = "unittesting"
    min_severity = 0.1
    max_severity = 3.9
    mean_remediate_low_severity = await get_mean_remediate_severity(
        context, project_name, min_severity, max_severity
    )
    expected_output = 181.0
    assert mean_remediate_low_severity == expected_output
    min_severity = 4
    max_severity = 6.9
    mean_remediate_medium_severity = await get_mean_remediate_severity(
        context, project_name, min_severity, max_severity
    )
    expected_output = 236
    assert mean_remediate_medium_severity == expected_output


@pytest.mark.changes_db
async def test_create_project_not_user_admin():
    await names_domain.create("NEWAVAILABLENAME", "group")
    user_email = "integratesuser@gmail.com"
    user_role = "customeradmin"
    test_data = await create_group(
        user_email=user_email,
        user_role=user_role,
        group_name="NEWAVAILABLENAME",
        organization="okada",
        description="This is a new project",
        has_skims=True,
        has_drills=True,
        has_forces=True,
        subscription="continuous",
    )
    expected_output = True
    assert test_data == expected_output


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "subscription",
        "has_skims",
        "has_drills",
        "has_forces",
        "has_integrates",
        "expected",
    ],
    [
        ["unittesting", "continuous", True, True, True, True, True],
        ["oneshottest", "oneshot", False, False, False, True, True],
        ["not-exists", "continuous", True, True, True, True, False],
        ["not-exists", "continuous", False, False, False, False, False],
    ],
)
async def test_edit(
    group_name: str,
    subscription: str,
    has_skims: bool,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    expected: bool,
):
    assert expected == await edit(
        context=get_new_context(),
        comments="",
        group_name=group_name,
        subscription=subscription,
        has_skims=has_skims,
        has_drills=has_drills,
        has_forces=has_forces,
        has_integrates=has_integrates,
        reason="",
        requester_email="test@test.test",
    )


async def test_get_pending_verification_findings():
    project_name = "unittesting"
    context = get_new_context()
    findings = await get_pending_verification_findings(context, project_name)
    assert len(findings) >= 1
    assert "finding" in findings[0]
    assert "finding_id" in findings[0]
    assert "project_name" in findings[0]


@freeze_time("2018-12-27")
async def test_get_total_comments_date():
    project_name = "unittesting"
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(project_name)
    total_comments = await get_total_comments_date(
        findings, project_name, last_day
    )
    assert total_comments == 5


@freeze_time("2021-05-12")
async def test_get_group_digest_stats():
    group_name = "unittesting"
    context = get_new_context()
    total_stats = await get_group_digest_stats(context, group_name)
    expected_output = {
        "group": group_name,
        "main": {
            "remediation_rate": 19,
            "reattack_effectiveness": 0,
            "remediation_time": 513,
            "comments": 0,
        },
        "reattacks": {
            "reattacks_requested": 0,
            "reattacks_executed": 0,
            "pending_attacks": 1,
        },
        "treatments": {
            "temporary_applied": 0,
            "eternal_requested": 0,
            "eternal_approved": 0,
        },
        "findings": [
            {
                "finding_name": "F007. Cross site request forgery",
                "finding_age": 847,
            }
        ],
    }
    assert expected_output == total_stats
