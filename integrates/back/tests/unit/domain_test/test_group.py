from back.tests.unit.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    InvalidGroupServicesConfig,
    RepeatedValues,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from events.domain import (
    list_group_events,
)
from findings.domain import (
    get_last_closed_vulnerability_info,
    get_max_open_severity,
    get_pending_verification_findings,
    get_total_treatment,
)
from freezegun import (  # type: ignore
    freeze_time,
)
from group_access.domain import (
    get_group_users,
    get_managers,
    get_reattackers,
    remove_access,
)
from group_comments.domain import (
    add_comment,
    get_total_comments_date,
    list_comments,
)
from groups.domain import (
    add_group,
    filter_active_groups,
    get_active_groups,
    get_alive_group_names,
    get_closed_vulnerabilities,
    get_description,
    get_group_digest_stats,
    get_groups_by_user,
    get_mean_remediate_non_treated_severity,
    get_mean_remediate_non_treated_severity_cvssf,
    get_mean_remediate_severity,
    get_mean_remediate_severity_cvssf,
    get_open_findings,
    get_open_vulnerabilities,
    get_vulnerabilities_with_pending_attacks,
    is_alive,
    update_group_attrs,
    validate_group_services_config,
    validate_group_tags,
)
from names import (
    domain as names_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.vulnerabilities import (
    get_closing_date,
    get_opening_date,
)
import pytest
from pytz import (  # type: ignore
    timezone,
)
from settings import (
    TIME_ZONE,
)
import time
from typing import (
    Optional,
    Tuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_group_services_config() -> None:
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, True, False)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(False, True, True)


@pytest.mark.changes_db
async def test_remove_access() -> None:
    loaders = get_new_context()
    assert await remove_access(loaders, "unittest", "unittesting")
    assert not await remove_access(loaders, "", "")


async def test_validate_tags() -> None:
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
        assert await validate_group_tags("unittesting", ["test-groups"])


async def test_is_alive() -> None:
    assert await is_alive("unittesting")
    assert not await is_alive("nonexistent_group")


async def test_get_vulnerabilities_with_pending_attacks() -> None:
    context = get_new_context()
    test_data = await get_vulnerabilities_with_pending_attacks(
        loaders=context, group_name="unittesting"
    )
    expected_output = 1
    assert test_data == expected_output


async def test_get_last_closed_vulnerability() -> None:
    findings_to_get = ["463558592", "422286126"]
    loaders: Dataloaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.finding.load_many(
        findings_to_get
    )
    (
        vuln_closed_days,
        last_closed_vuln,
    ) = await get_last_closed_vulnerability_info(loaders, findings)
    tzn = timezone(TIME_ZONE)
    actual_date = datetime.now(tz=tzn).date()
    initial_date = datetime(2019, 1, 15).date()
    assert vuln_closed_days == (actual_date - initial_date).days
    assert last_closed_vuln.id == "242f848c-148a-4028-8e36-c7d995502590"
    assert last_closed_vuln.finding_id == "463558592"


async def test_get_vuln_closing_date() -> None:
    closed_vulnerability = Vulnerability(
        finding_id="422286126",
        id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        specific="phone",
        state=VulnerabilityState(
            modified_by="test@test.com",
            modified_date="2019-01-08T21:01:26+00:00",
            source=Source.ASM,
            status=VulnerabilityStateStatus.CLOSED,
        ),
        type=VulnerabilityType.INPUTS,
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_report_date="2019-01-08T21:01:26+00:00",
            unreliable_source=Source.ASM,
        ),
        where="https://example.com",
    )
    test_data = get_closing_date(closed_vulnerability)
    closing_date = datetime(2019, 1, 8).date()
    assert test_data == closing_date

    loaders: Dataloaders = get_new_context()
    open_vulnerability: Vulnerability = await loaders.vulnerability.load(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )
    test_data = get_closing_date(open_vulnerability)
    assert test_data is None


async def test_get_max_open_severity() -> None:
    findings_to_get = ["463558592", "422286126"]
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.finding.load_many(
        findings_to_get
    )
    test_data = await get_max_open_severity(loaders, findings)
    assert test_data[0] == Decimal(4.3).quantize(Decimal("0.1"))
    assert test_data[1].id == "463558592"


async def test_get_open_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 29
    open_vulns = await get_open_vulnerabilities(get_new_context(), group_name)
    assert open_vulns == expected_output


async def test_get_closed_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 7
    closed_vulnerabilities = await get_closed_vulnerabilities(
        get_new_context(), group_name
    )
    assert closed_vulnerabilities == expected_output


async def test_get_open_findings() -> None:
    group_name = "unittesting"
    expected_output = 5
    open_findings = await get_open_findings(get_new_context(), group_name)
    assert open_findings == expected_output


async def test_get_vuln_opening_date() -> None:
    test_vuln = Vulnerability(
        finding_id="",
        id="",
        specific="",
        type=VulnerabilityType.LINES,
        where="",
        state=VulnerabilityState(
            modified_by="",
            modified_date="2019-01-08T21:01:26+00:00",
            source=Source.ASM,
            status=VulnerabilityStateStatus.OPEN,
        ),
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_report_date="2019-01-08T21:01:26+00:00",
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        ),
    )
    result_date = get_opening_date(test_vuln)
    assert result_date == datetime(2019, 1, 8).date()

    min_date = datetime(2021, 1, 1).date()
    result_date = get_opening_date(vuln=test_vuln, min_date=min_date)
    assert result_date is None

    loaders: Dataloaders = get_new_context()
    test_open_vuln = await loaders.vulnerability.load(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )
    result_date = get_opening_date(test_open_vuln)
    expected_output = datetime(2020, 9, 9).date()
    assert result_date == expected_output


@freeze_time("2020-12-01")
async def test_get_mean_remediate() -> None:
    context = get_new_context()
    group_name = "unittesting"
    min_severity: Decimal = Decimal("0.0")
    max_severity: Decimal = Decimal("10.0")
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity
    ) == Decimal("384.0")
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity
    ) == Decimal("386.0")

    min_date = datetime_utils.get_now_minus_delta(days=30).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")

    min_date = datetime_utils.get_now_minus_delta(days=90).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("82.0")
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("376.001")),
        (30, Decimal("0")),
        (90, Decimal("82.000")),
    ),
)
async def test_get_mean_remediate_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    mean_remediate_cvssf = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        Decimal("0.0"),
        Decimal("10.0"),
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_cvssf == expected_output


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("239.007")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_non_treated_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    mttr_no_treated_cvssf = (
        await get_mean_remediate_non_treated_severity_cvssf(
            loaders,
            group_name,
            Decimal("0.0"),
            Decimal("10.0"),
            (datetime.now() - timedelta(days=min_days)).date()
            if min_days
            else None,
        )
    )
    assert mttr_no_treated_cvssf == expected_output


async def test_get_total_treatment() -> None:
    loaders = get_new_context()
    findings_to_get = ["463558592", "422286126"]
    findings: Tuple[Finding, ...] = await loaders.finding.load_many(
        findings_to_get
    )
    test_data = await get_total_treatment(loaders, findings)
    expected_output = {
        "inProgress": 1,
        "accepted": 1,
        "acceptedUndefined": 0,
        "undefined": 0,
    }
    assert test_data == expected_output


async def test_list_comments() -> None:
    group_name = "unittesting"
    test_data = await list_comments(group_name, "admin")
    expected_output = {
        "content": "Now we can post comments on groups",
        "parent": 0,
        "created": "2018/12/27 16:30:28",
        "id": 1545946228675,
        "fullname": "Miguel de Orellana at Fluid Attacks",
        "email": "unittest@fluidattacks.com",
        "modified": "2018/12/27 16:30:28",
    }
    assert test_data[0] == expected_output


@pytest.mark.changes_db
async def test_add_comment() -> None:
    group_name = "unittesting"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = int(round(time.time() * 1000))
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    comment_data = {
        "user_id": comment_id,
        "content": "Test comment",
        "created": current_time,
        "fullname": "unittesting",
        "modified": current_time,
        "parent": "0",
    }
    assert await add_comment(
        info, group_name, "unittest@fluidattacks.com", comment_data
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_data["created"] = current_time
    comment_data["modified"] = current_time
    comment_data["parent"] = str(comment_id)
    assert await add_comment(
        info, group_name, "unittest@fluidattacks.com", comment_data
    )


async def test_get_active_groups() -> None:
    test_data = await get_active_groups()
    assert test_data is not None


async def test_get_alive_group_names() -> None:
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


async def test_list_events() -> None:
    group_name = "unittesting"
    expected_output = [
        "540462628",
        "538745942",
        "463578352",
        "484763304",
        "418900971",
    ]
    assert expected_output == await list_group_events(group_name)


async def test_get_managers() -> None:
    group_name = "unittesting"
    expected_output = [
        "integratesuser@gmail.com",
        "continuoushacking@gmail.com",
        "continuoushack2@gmail.com",
    ]
    assert expected_output == await get_managers(group_name)


async def test_get_description() -> None:
    group_name = "unittesting"
    expected_output = "Integrates unit test group"
    assert expected_output == await get_description(group_name)


async def test_get_users() -> None:
    group_name = "unittesting"
    users = await get_group_users(group_name)
    expected = [
        "integratesserviceforces@gmail.com",
        "integratesmanager@gmail.com",
        "unittest@fluidattacks.com",
        "integrateshacker@fluidattacks.com",
        "integratesreattacker@fluidattacks.com",
        "unittest2@fluidattacks.com",
        "customer_manager@fluidattacks.com",
        "integratesexecutive@gmail.com",
        "integratesuser2@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integratesuser@gmail.com",
        "continuoushacking@gmail.com",
        "integratesmanager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "continuoushack2@gmail.com",
        "integratesreviewer@fluidattacks.com",
    ]
    for user in expected:
        assert user in users


async def test_get_reattackers() -> None:
    reattackers = await get_reattackers("oneshottest")
    assert reattackers == ["integrateshacker@fluidattacks.com"]


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("10")),
        (30, Decimal("0")),
        (90, Decimal("1")),
    ),
)
async def test_get_mean_remediate_severity_low_min_days(
    min_days: Optional[int], expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    mean_remediate_low_severity = await get_mean_remediate_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_low_severity == expected_output


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("49.797")),
        (30, Decimal("10.658")),
        (90, Decimal("11.269")),
    ),
)
async def test_get_mean_remediate_severity_low(
    min_days: Optional[int], expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    low_severity = await get_mean_remediate_non_treated_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert low_severity == expected_output


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("185")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_severity_medium(
    min_days: Optional[int], expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("4.0")
    max_severity = Decimal("6.9")
    mean_remediate_medium_severity = await get_mean_remediate_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_medium_severity == expected_output


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("182")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_non_treated_severity_medium(
    min_days: Optional[int], expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("4.0")
    max_severity = Decimal("6.9")
    medium_severity = await get_mean_remediate_non_treated_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert medium_severity == expected_output


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("152.580")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_severity_medium_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("4")
    max_severity = Decimal("6.9")
    mean_remediate_medium_severity = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_medium_severity == expected_output


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("364.485")),
        (30, Decimal("0.0")),
        (90, Decimal("82.0")),
    ),
)
async def test_get_mean_remediate_severity_low_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    mean_remediate_low_severity = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_low_severity == expected_output


@pytest.mark.changes_db
async def test_create_group_not_user_admin() -> None:
    await names_domain.create("NEWAVAILABLENAME", "group")
    user_email = "integratesuser@gmail.com"
    user_role = "user_manager"
    test_data = await add_group(
        user_email=user_email,
        user_role=user_role,
        group_name="NEWAVAILABLENAME",
        organization="okada",
        description="This is a new group",
        has_machine=True,
        has_squad=True,
        service="WHITE",
        subscription="continuous",
    )
    expected_output = True
    assert test_data == expected_output


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_asm",
        "expected",
        "tier",
    ],
    [
        [
            "unittesting",
            "WHITE",
            "continuous",
            True,
            True,
            True,
            True,
            "SQUAD",
        ],
        [
            "oneshottest",
            "BLACK",
            "oneshot",
            False,
            False,
            True,
            True,
            "ONESHOT",
        ],
        [
            "not-exists",
            "WHITE",
            "continuous",
            True,
            True,
            True,
            False,
            "MACHINE",
        ],
        [
            "not-exists",
            "WHITE",
            "continuous",
            False,
            False,
            False,
            False,
            "FREE",
        ],
    ],  # pylint: disable=too-many-arguments
)
async def test_update_group_attrs(
    group_name: str,
    service: str,
    subscription: str,
    has_machine: bool,
    has_squad: bool,
    has_asm: bool,
    expected: bool,
    tier: str,
) -> None:
    assert expected == await update_group_attrs(
        loaders=get_new_context(),
        comments="",
        group_name=group_name,
        subscription=subscription,
        has_machine=has_machine,
        has_squad=has_squad,
        has_asm=has_asm,
        reason="",
        requester_email="test@test.test",
        service=service,
        tier=tier,
    )


async def test_get_pending_verification_findings() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    findings = await get_pending_verification_findings(loaders, group_name)
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"


@freeze_time("2018-12-27")
async def test_get_total_comments_date() -> None:
    group_name = "unittesting"
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_ids = list(map(lambda finding: finding.id, findings))
    total_comments = await get_total_comments_date(
        findings_ids, group_name, last_day
    )
    assert total_comments == 5


@freeze_time("2021-05-12")
async def test_get_group_digest_stats() -> None:
    group_name = "unittesting"
    context = get_new_context()
    total_stats = await get_group_digest_stats(context, group_name)
    expected_output = {
        "group": group_name,
        "main": {
            "group_age": 356,
            "remediation_rate": 19,
            "remediation_time": 515,
            "comments": 0,
        },
        "reattacks": {
            "effective_reattacks": 0,
            "effective_reattacks_total": 0,
            "reattacks_requested": 0,
            "last_requested_date": "2020-02-19 10:41:04",
            "reattacks_executed": 0,
            "reattacks_executed_total": 1,
            "last_executed_date": "2020-02-19 10:41:04",
            "pending_attacks": 1,
        },
        "treatments": {
            "temporary_applied": 0,
            "permanent_requested": 0,
            "permanent_approved": 0,
            "undefined": 0,
        },
        "events": {
            "unsolved": 3,
            "new": 0,
        },
        "findings": [
            {
                "oldest_name": "038. Business information leak",
                "oldest_age": 620,
                "severest_name": "014. Insecure functionality",
                "severity": "6.3",
            }
        ],
        "vulns_len": 36,
    }
    assert expected_output == total_stats


async def test_get_groups_by_user() -> None:
    loaders = get_new_context()
    expected_groups = [
        "asgard",
        "barranquilla",
        "gotham",
        "metropolis",
        "oneshottest",
        "monteria",
        "unittesting",
    ]
    user_groups = await get_groups_by_user("integratesmanager@gmail.com")
    groups = await loaders.group.load_many(user_groups)
    groups_filtered = filter_active_groups(groups)
    assert sorted([group["name"] for group in groups_filtered]) == sorted(
        expected_groups
    )

    expected_org_groups = ["oneshottest", "unittesting"]
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    user_org_groups = await get_groups_by_user(
        "integratesmanager@gmail.com", organization_id=org_id
    )
    groups = await loaders.group.load_many(user_org_groups)
    groups_filtered = filter_active_groups(groups)
    assert sorted([group["name"] for group in groups_filtered]) == sorted(
        expected_org_groups
    )
