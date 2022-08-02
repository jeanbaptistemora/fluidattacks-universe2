# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    GroupNotFound,
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
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupTreatmentSummary,
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
from findings.domain import (
    get_last_closed_vulnerability_info,
    get_max_open_severity,
    get_pending_verification_findings,
)
from freezegun import (  # type: ignore
    freeze_time,
)
from group_access.domain import (
    exists,
    get_group_stakeholders_emails,
    get_managers,
    get_reattackers,
    remove_access,
)
from group_comments.domain import (
    add_comment,
    list_comments,
)
from groups.domain import (
    add_group,
    get_closed_vulnerabilities,
    get_groups_by_stakeholder,
    get_mean_remediate_non_treated_severity,
    get_mean_remediate_non_treated_severity_cvssf,
    get_mean_remediate_severity,
    get_mean_remediate_severity_cvssf,
    get_open_findings,
    get_open_vulnerabilities,
    get_treatment_summary,
    get_vulnerabilities_with_pending_attacks,
    is_valid,
    remove_pending_deletion_date,
    send_mail_devsecops_agent,
    set_pending_deletion_date,
    update_group,
    validate_group_services_config,
    validate_group_tags,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.datetime import (
    convert_from_iso_str,
    is_valid_format,
)
from newutils.groups import (
    filter_active_groups,
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
    loaders: Dataloaders = get_new_context()
    email = "unittest@fluidattacks.com"
    group_name = "unittesting"
    assert await exists(loaders, group_name, email)
    assert await remove_access(loaders, email, group_name)

    loaders = get_new_context()
    assert not await exists(loaders, group_name, email)


async def test_validate_tags() -> None:
    loaders: Dataloaders = get_new_context()
    assert await validate_group_tags(
        loaders, "unittesting", ["testtag", "this-is-ok", "th15-4l50"]
    )
    assert await validate_group_tags(
        loaders, "unittesting", ["this-tag-is-valid", "but this is not"]
    ) == ["this-tag-is-valid"]
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags(
            loaders, "unittesting", ["same-name", "same-name", "another-one"]
        )
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags(
            loaders, "unittesting", ["test-groups"]
        )


async def test_is_valid() -> None:
    loaders: Dataloaders = get_new_context()
    assert await is_valid(loaders, "unittesting")
    assert not await is_valid(loaders, "nonexistent_group")


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
        group_name="unittesting",
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
        group_name="",
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


async def test_get_treatment_summary() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    test_data = await get_treatment_summary(loaders, group_name)
    expected_output = GroupTreatmentSummary(
        accepted=2,
        accepted_undefined=1,
        in_progress=1,
        new=25,
    )
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


async def test_list_events() -> None:
    group_name = "unittesting"
    expected_output = [
        "418900971",
        "463578352",
        "484763304",
        "538745942",
        "540462628",
        "540462638",
    ]
    loaders: Dataloaders = get_new_context()
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    assert expected_output == sorted([event.id for event in events_group])


async def test_get_managers() -> None:
    group_name = "unittesting"
    expected_output = [
        "integratesuser@gmail.com",
        "vulnmanager@gmail.com",
        "continuoushacking@gmail.com",
        "continuoushack2@gmail.com",
    ]
    assert expected_output == await get_managers(get_new_context(), group_name)


async def test_get_users() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    users = await get_group_stakeholders_emails(loaders, group_name)
    expected = [
        "integratesserviceforces@gmail.com",
        "integratesmanager@gmail.com",
        "unittest@fluidattacks.com",
        "integrateshacker@fluidattacks.com",
        "integratesreattacker@fluidattacks.com",
        "unittest2@fluidattacks.com",
        "customer_manager@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integratesuser@gmail.com",
        "continuoushacking@gmail.com",
        "integratesmanager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "continuoushack2@gmail.com",
        "integratesreviewer@fluidattacks.com",
        "vulnmanager@gmail.com",
    ]
    for user in expected:
        assert user in users


async def test_get_reattackers() -> None:
    reattackers = await get_reattackers(get_new_context(), "oneshottest")
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
    user_email = "integratesuser@gmail.com"
    user_role = "user_manager"
    await add_group(
        loaders=get_new_context(),
        description="This is a new group",
        group_name="newavailablename",
        has_machine=True,
        has_squad=True,
        organization_name="okada",
        service=GroupService.WHITE,
        subscription=GroupSubscriptionType.CONTINUOUS,
        user_email=user_email,
        user_role=user_role,
    )


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_asm",
        "tier",
    ],
    [
        [
            "unittesting",
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            True,
            True,
            True,
            GroupTier.SQUAD,
        ],
        [
            "oneshottest",
            GroupService.BLACK,
            GroupSubscriptionType.ONESHOT,
            False,
            False,
            True,
            GroupTier.ONESHOT,
        ],
    ],  # pylint: disable=too-many-arguments
)
async def test_update_group_attrs(
    group_name: str,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_asm: bool,
    tier: GroupTier,
) -> None:
    await update_group(
        loaders=get_new_context(),
        comments="",
        group_name=group_name,
        justification=GroupStateUpdationJustification.NONE,
        has_asm=has_asm,
        has_machine=has_machine,
        has_squad=has_squad,
        service=service,
        subscription=subscription,
        tier=tier,
        user_email="test@test.test",
    )


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_asm",
        "tier",
    ],
    [
        [
            "not-exists",
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            True,
            True,
            True,
            GroupTier.MACHINE,
        ],
        [
            "not-exists",
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            False,
            False,
            False,
            GroupTier.FREE,
        ],
    ],  # pylint: disable=too-many-arguments
)
async def test_update_group_attrs_fail(
    group_name: str,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_asm: bool,
    tier: GroupTier,
) -> None:
    with pytest.raises(GroupNotFound):
        await update_group(
            loaders=get_new_context(),
            comments="",
            group_name=group_name,
            justification=GroupStateUpdationJustification.NONE,
            has_asm=has_asm,
            has_machine=has_machine,
            has_squad=has_squad,
            service=service,
            subscription=subscription,
            tier=tier,
            user_email="test@test.test",
        )


async def test_get_pending_verification_findings() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    findings = await get_pending_verification_findings(loaders, group_name)
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"


async def test_get_groups_by_user() -> None:
    loaders: Dataloaders = get_new_context()
    expected_groups = [
        "asgard",
        "barranquilla",
        "gotham",
        "metropolis",
        "oneshottest",
        "monteria",
        "unittesting",
    ]
    user_groups_names = await get_groups_by_stakeholder(
        loaders, "integratesmanager@gmail.com"
    )
    groups: tuple[Group, ...] = await loaders.group.load_many(
        user_groups_names
    )
    groups_filtered = filter_active_groups(groups)
    assert sorted([group.name for group in groups_filtered]) == sorted(
        expected_groups
    )

    expected_org_groups = ["oneshottest", "unittesting"]
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    user_org_groups_names = await get_groups_by_stakeholder(
        loaders, "integratesmanager@gmail.com", organization_id=org_id
    )
    groups = await loaders.group.load_many(user_org_groups_names)
    groups_filtered = filter_active_groups(groups)
    assert sorted([group.name for group in groups_filtered]) == sorted(
        expected_org_groups
    )


@pytest.mark.changes_db
async def test_set_pending_deletion_date() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    user_email = "integratesmanager@gmail.com"
    test_date = "2022-04-06T16:46:23+00:00"
    group: Group = await loaders.group.load(group_name)
    assert group.state.pending_deletion_date is None

    await set_pending_deletion_date(
        group=group, modified_by=user_email, pending_deletion_date=test_date
    )
    loaders.group.clear(group_name)
    group_updated: Group = await loaders.group.load(group_name)
    assert is_valid_format(
        convert_from_iso_str(group_updated.state.pending_deletion_date)
    )
    assert group_updated.state.pending_deletion_date == test_date
    assert group_updated.state.modified_by == user_email


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "responsible",
        "had_token",
    ],
    [
        [
            "unittesting",
            "integratesmanager@gmail.com",
            True,
        ],
        [
            "unittesting",
            "integratesmanager@gmail.com",
            False,
        ],
    ],
)
async def test_send_mail_devsecops_agent(
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    await send_mail_devsecops_agent(
        loaders=get_new_context(),
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "responsible",
        "had_token",
    ],
    [
        [
            "not-exist",
            "integratesmanager@gmail.com",
            True,
        ],
        [
            "not-exist",
            "integratesmanager@gmail.com",
            False,
        ],
    ],
)
async def test_send_mail_devsecops_agent_fail(
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    with pytest.raises(GroupNotFound):
        await send_mail_devsecops_agent(
            loaders=get_new_context(),
            group_name=group_name,
            responsible=responsible,
            had_token=had_token,
        )


@pytest.mark.changes_db
async def test_clear_pending_deletion_date() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    user_email = "integratesmanager@gmail.com"
    group: Group = await loaders.group.load(group_name)
    assert group.state.pending_deletion_date

    await remove_pending_deletion_date(group=group, modified_by=user_email)
    loaders.group.clear(group_name)
    group_updated: Group = await loaders.group.load(group_name)
    assert group_updated.state.pending_deletion_date is None
    assert group_updated.state.modified_by == user_email
