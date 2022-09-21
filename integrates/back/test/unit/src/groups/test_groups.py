# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateRemovalJustification,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupTreatmentSummary,
)
from groups.domain import (
    add_group,
    get_closed_vulnerabilities,
    get_groups_by_stakeholder,
    get_open_findings,
    get_open_vulnerabilities,
    get_treatment_summary,
    get_vulnerabilities_with_pending_attacks,
    is_valid,
    remove_group,
    update_group,
    validate_group_tags,
)
from newutils.groups import (
    filter_active_groups,
)
from organizations import (
    domain as orgs_domain,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_tags() -> None:
    loaders: Dataloaders = get_new_context()
    assert await validate_group_tags(
        loaders, "unittesting", ["testtag", "this-is-ok", "th15-4l50"]
    )
    assert await validate_group_tags(
        loaders, "unittesting", ["this-tag-is-valid", "but this is not"]
    ) == ["this-tag-is-valid"]


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


@pytest.mark.changes_db
async def test_create_group_not_user_admin() -> None:
    user_email = "integratesuser@gmail.com"
    user_role = "user_manager"
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_group_names(loaders)
    assert len(active_groups) == 15
    await add_group(
        loaders=loaders,
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
    active_groups = await orgs_domain.get_all_active_group_names(
        loaders=get_new_context()
    )
    assert len(active_groups) == 16
    await remove_group(
        loaders=get_new_context(),
        group_name="newavailablename",
        justification=GroupStateRemovalJustification.OTHER,
        user_email=user_email,
    )
    active_groups = await orgs_domain.get_all_active_group_names(
        loaders=get_new_context()
    )
    assert len(active_groups) == 15


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
    ],  # pylint: disable=too-many-arguments
)
async def test_update_group_attrs(
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
        group_name=group_name,
        justification=GroupStateUpdationJustification.NONE,
        has_arm=has_arm,
        has_machine=has_machine,
        has_squad=has_squad,
        service=service,
        subscription=subscription,
        tier=tier,
        user_email="integratesmanager@fluidattacks.com",
    )
