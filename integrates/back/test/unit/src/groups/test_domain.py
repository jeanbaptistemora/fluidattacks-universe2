from aioextensions import (
    collect,
)
from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
    set_mocks_return_values,
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
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateJustification,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
    GroupTreatmentSummary,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
from groups.domain import (
    add_group,
    get_closed_vulnerabilities,
    get_group,
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
    remove_group,
    remove_pending_deletion_date,
    send_mail_devsecops_agent,
    set_pending_deletion_date,
    update_group,
    validate_group_services_config,
    validate_group_services_config_deco,
    validate_group_tags,
)
import json
from newutils import (
    datetime as datetime_utils,
)
from newutils.groups import (
    filter_active_groups,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_create_group_not_user_admin() -> None:
    email = "integratesuser@gmail.com"
    granted_role = "user_manager"
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_group_names(loaders)
    assert len(active_groups) == 14
    await add_group(
        loaders=loaders,
        description="This is a new group",
        email=email,
        granted_role=granted_role,
        group_name="newavailablename",
        has_machine=True,
        has_squad=True,
        organization_name="okada",
        service=GroupService.WHITE,
        subscription=GroupSubscriptionType.CONTINUOUS,
    )
    active_groups = await orgs_domain.get_all_active_group_names(
        loaders=get_new_context()
    )
    assert len(active_groups) == 15
    await remove_group(
        loaders=get_new_context(),
        group_name="newavailablename",
        justification=GroupStateJustification.OTHER,
        email=email,
    )
    active_groups = await orgs_domain.get_all_active_group_names(
        loaders=get_new_context()
    )
    assert len(active_groups) == 14


async def test_get_closed_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 7
    closed_vulnerabilities = await get_closed_vulnerabilities(
        get_new_context(), group_name
    )
    assert closed_vulnerabilities == expected_output


async def test_get_groups_by_stakeholder() -> None:
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
    groups = await collect(
        [
            get_group(loaders, user_group_name)
            for user_group_name in user_groups_names
        ]
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
    groups = await collect(
        [
            get_group(loaders, user_org_group_name)
            for user_org_group_name in user_org_groups_names
        ]
    )
    groups_filtered = filter_active_groups(groups)
    assert sorted([group.name for group in groups_filtered]) == sorted(
        expected_org_groups
    )


@freeze_time("2020-12-01")
async def test_get_mean_remediate_non_treated_severity() -> None:
    context = get_new_context()
    group_name = "unittesting"
    min_severity: Decimal = Decimal("0.0")
    max_severity: Decimal = Decimal("10.0")
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity
    ) == Decimal("387.0")

    min_date = datetime_utils.get_now_minus_delta(days=30).date()
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")

    min_date = datetime_utils.get_now_minus_delta(days=90).date()
    assert await get_mean_remediate_non_treated_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("183")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_non_treated_severity_medium(
    min_days: int | None, expected_output: Decimal
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
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert medium_severity == expected_output


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("238.671")),
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
            (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
            if min_days
            else None,
        )
    )
    assert mttr_no_treated_cvssf == expected_output


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    [
        "group_name",
        "min_severity",
        "max_severity",
        "min_days",
        "expected_output",
    ],
    [
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            0,
            Decimal("375.797"),
        ],
        ["unittesting", Decimal("0.0"), Decimal("10.0"), 30, Decimal("0")],
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            90,
            Decimal("83.0"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            0,
            Decimal("365.252"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            30,
            Decimal("0.0"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            90,
            Decimal("83.0"),
        ],
        [
            "unittesting",
            Decimal("4"),
            Decimal("6.9"),
            0,
            Decimal("377.003"),
        ],
        [
            "unittesting",
            Decimal("4"),
            Decimal("6.9"),
            30,
            Decimal("0"),
        ],
        [
            "unittesting",
            Decimal("4"),
            Decimal("6.9"),
            90,
            Decimal("0"),
        ],
    ],
)
@patch(
    get_mocked_path("loaders.finding_vulnerabilities.load_many_chained"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("loaders.group_findings.load"), new_callable=AsyncMock)
async def test_get_mean_remediate_cvssf(  # pylint: disable=too-many-arguments
    mock_group_findings_loader: AsyncMock,
    mock_finding_vulnerabilities_load_many_chained: AsyncMock,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_days: int,
    expected_output: Decimal,
) -> None:
    mock_group_findings_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group_findings.load"),
        json.dumps([group_name]),
    )
    mock_finding_vulnerabilities_load_many_chained.return_value = (
        get_mock_response(
            get_mocked_path(
                "loaders.finding_vulnerabilities.load_many_chained"
            ),
            json.dumps([group_name, min_severity, max_severity], default=str),
        )
    )
    loaders = get_new_context()
    mean_remediate_cvssf = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mock_group_findings_loader.called is True
    assert mock_finding_vulnerabilities_load_many_chained.called is True
    assert mean_remediate_cvssf == expected_output


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("50.557")),
        (30, Decimal("11.534")),
        (90, Decimal("12.149")),
    ),
)
async def test_get_mean_remediate_severity_low(
    min_days: int | None, expected_output: Decimal
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
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert low_severity == expected_output


@freeze_time("2020-12-01")
async def test_get_mean_remediate_severity() -> None:
    context = get_new_context()
    group_name = "unittesting"
    min_severity: Decimal = Decimal("0.0")
    max_severity: Decimal = Decimal("10.0")
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity
    ) == Decimal("385.0")

    min_date = datetime_utils.get_now_minus_delta(days=30).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")

    min_date = datetime_utils.get_now_minus_delta(days=90).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("83.0")


async def test_get_open_findings() -> None:
    group_name = "unittesting"
    expected_output = 5
    open_findings = await get_open_findings(get_new_context(), group_name)
    assert open_findings == expected_output


async def test_get_open_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 29
    open_vulns = await get_open_vulnerabilities(get_new_context(), group_name)
    assert open_vulns == expected_output


async def test_get_treatment_summary() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    test_data = await get_treatment_summary(loaders, group_name)
    expected_output = GroupTreatmentSummary(
        accepted=2,
        accepted_undefined=1,
        in_progress=1,
        untreated=25,
    )
    assert test_data == expected_output


async def test_get_vulnerabilities_with_pending_attacks() -> None:
    context = get_new_context()
    test_data = await get_vulnerabilities_with_pending_attacks(
        loaders=context, group_name="unittesting"
    )
    expected_output = 1
    assert test_data == expected_output


async def test_is_valid() -> None:
    loaders: Dataloaders = get_new_context()
    assert await is_valid(loaders, "unittesting")
    assert not await is_valid(loaders, "nonexistent_group")


@pytest.mark.parametrize(
    ["group", "user_email"],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                name="unittesting",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags={"test-updates", "test-tag", "test-groups"},
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.WHITE,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context="Group context test",
                disambiguation="Disambiguation test",
                files=[],
                policies=None,
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat(
                    "2022-08-06T19:28:00+00:00"
                ),
            ),
            "integratesmanager@gmail.com",
        ],
    ],
)
@patch(get_mocked_path("update_state"), new_callable=AsyncMock)
async def test_remove_pending_deletion_date(
    mock_groups_domain_update_state: AsyncMock,
    group: Group,
    user_email: str,
) -> None:

    mock_groups_domain_update_state.return_value = get_mock_response(
        get_mocked_path("update_state"),
        json.dumps([group.name, user_email], default=str),
    )
    await remove_pending_deletion_date(group=group, modified_by=user_email)

    assert mock_groups_domain_update_state.called is True


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
@patch(
    get_mocked_path("mailer_utils.get_group_emails_by_notification"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("groups_mail.send_mail_devsecops_agent_token"),
    new_callable=AsyncMock,
)
async def test_send_mail_devsecops_agent(
    mock_mailer_utils_get_group_emails_by_notification: AsyncMock,
    mock_groups_mail_send_mail_devsecops_agent_token: AsyncMock,
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:

    mocks_args: list[list[Any]]
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_mailer_utils_get_group_emails_by_notification,
            mock_groups_mail_send_mail_devsecops_agent_token,
        ],
        [
            "mailer_utils.get_group_emails_by_notification",
            "groups_mail.send_mail_devsecops_agent_token",
        ],
        [
            [group_name, "devsecops_agent"],
            [responsible, group_name, had_token],
        ],
    ]

    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    await send_mail_devsecops_agent(
        loaders=get_new_context(),
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ["group", "user_email", "date"],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                name="unittesting",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags={"test-updates", "test-tag", "test-groups"},
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.WHITE,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context="Group context test",
                disambiguation="Disambiguation test",
                files=[],
                policies=None,
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat(
                    "2022-08-06T19:28:00+00:00"
                ),
            ),
            "integratesmanager@gmail.com",
            datetime.fromisoformat("2022-04-06T16:46:23+00:00"),
        ],
    ],
)
@patch(get_mocked_path("update_state"), new_callable=AsyncMock)
async def test_set_pending_deletion_date(
    mock_groups_domain_update_state: AsyncMock,
    group: Group,
    user_email: str,
    date: datetime,
) -> None:

    mock_groups_domain_update_state.return_value = get_mock_response(
        get_mocked_path("update_state"),
        json.dumps(
            [group.name, group.organization_id, user_email, date], default=str
        ),
    )
    await set_pending_deletion_date(
        group=group, modified_by=user_email, pending_deletion_date=date
    )

    assert mock_groups_domain_update_state.called is True


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_arm",
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
    ],
)
async def test_update_group(
    # pylint: disable=too-many-arguments
    group_name: str,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
    tier: GroupTier,
) -> None:
    await update_group(
        loaders=get_new_context(),
        comments="",
        email="integratesmanager@fluidattacks.com",
        group_name=group_name,
        justification=GroupStateJustification.NONE,
        has_arm=has_arm,
        has_machine=has_machine,
        has_squad=has_squad,
        service=service,
        subscription=subscription,
        tier=tier,
    )


@pytest.mark.parametrize(
    ["group_name", "tags", "tags_to_raise_exception"],
    [
        [
            "unittesting",
            ["testtag", "this-is-ok", "th15-4l50"],
            ["same-name", "same-name", "another-one"],
        ],
        [
            "unittesting",
            ["this-tag-is-valid", "but this is not"],
            ["test-groups"],
        ],
    ],
)
@patch(MODULE_AT_TEST + "_has_repeated_tags")
async def test_validate_group_tags(
    mock__has_repeated_tags: AsyncMock,
    group_name: str,
    tags: list,
    tags_to_raise_exception: list,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[group_name, tags]],
        mocked_objects=[mock__has_repeated_tags],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_has_repeated_tags"],
    )
    loaders: Dataloaders = get_new_context()
    result = await validate_group_tags(loaders, group_name, tags)
    assert isinstance(result, list)
    assert mock__has_repeated_tags.called is True

    assert set_mocks_return_values(
        mocks_args=[[group_name, tags_to_raise_exception]],
        mocked_objects=[mock__has_repeated_tags],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_has_repeated_tags"],
    )
    with pytest.raises(RepeatedValues):
        await validate_group_tags(loaders, group_name, tags_to_raise_exception)
    assert mock__has_repeated_tags.call_count == 2


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("11")),
        (30, Decimal("1")),
        (90, Decimal("2")),
    ),
)
async def test_get_mean_remediate_severity_low_min_days(
    min_days: int | None, expected_output: Decimal
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
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_low_severity == expected_output


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("186")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_severity_medium(
    min_days: int | None, expected_output: Decimal
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
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_medium_severity == expected_output


@pytest.mark.parametrize(
    ["has_machine", "has_squad", "has_arm"],
    [
        [
            True,
            True,
            True,
        ],
    ],
)
def test_validate_group_services_config(
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
) -> None:
    validate_group_services_config(has_machine, has_squad, has_arm)

    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_asm:
        validate_group_services_config(
            has_machine=True, has_squad=True, has_arm=False
        )
    assert (
        str(invalid_group_service_asm.value)
        == "Exception - Squad is only available when ASM is too"
    )

    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_machine:
        validate_group_services_config(
            has_machine=False, has_squad=True, has_arm=True
        )
    assert (
        str(invalid_group_service_machine.value)
        == "Exception - Squad is only available when Machine is too"
    )


def test_validate_group_services_config_deco() -> None:
    @validate_group_services_config_deco(
        has_machine_field="has_machine",
        has_squad_field="has_squad",
        has_arm_field="has_arm",
    )
    def decorated_func(
        has_machine: bool, has_squad: bool, has_arm: bool
    ) -> str:
        return str(has_machine and has_squad and has_arm)

    assert decorated_func(has_machine=True, has_squad=True, has_arm=True)
    assert decorated_func(has_machine=False, has_squad=False, has_arm=False)
    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_asm:
        decorated_func(has_machine=True, has_squad=True, has_arm=False)
    assert (
        str(invalid_group_service_asm.value)
        == "Exception - Squad is only available when ASM is too"
    )
    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_machine:
        decorated_func(has_machine=False, has_squad=True, has_arm=True)
    assert (
        str(invalid_group_service_machine.value)
        == "Exception - Squad is only available when Machine is too"
    )
