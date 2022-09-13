# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    GroupNotFound,
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptances,
    InvalidOrganization,
    InvalidSeverity,
    InvalidVulnerabilityGracePeriod,
    OrganizationNotFound,
    StakeholderNotInOrganization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.types import (
    PoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as group_domain,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.domain import (
    iterate_organizations_and_groups,
)
import pytest
from typing import (
    Any,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_customer_manager_good() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    user = "org_testgroupmanager2@fluidattacks.com"
    assert not await orgs_domain.has_access(loaders, org_id, user)

    await orgs_domain.add_stakeholder(
        loaders, org_id, user, "customer_manager"
    )
    assert (
        await authz.get_organization_level_role(
            get_new_context(), user, org_id
        )
        == "customer_manager"
    )

    loaders = get_new_context()
    group_names = await orgs_domain.get_group_names(loaders, org_id)
    groups_users = await collect(
        group_access_domain.get_group_stakeholders_emails(loaders, group)
        for group in group_names
    )
    assert all(user in group_users for group_users in groups_users)


@pytest.mark.changes_db
async def test_add_organization() -> None:
    loaders: Dataloaders = get_new_context()
    org_name = "esdeath"
    user = "org_testusermanager1@gmail.com"
    with pytest.raises(OrganizationNotFound):
        await loaders.organization.load(org_name)

    await orgs_domain.add_organization(loaders, org_name, user)

    organization: Organization = await loaders.organization.load(org_name)
    loaders = get_new_context()
    assert await orgs_domain.has_access(loaders, organization.id, user)
    assert (
        await authz.get_organization_level_role(loaders, user, organization.id)
        == "user_manager"
    )

    with pytest.raises(InvalidOrganization):
        await orgs_domain.add_organization(loaders, org_name, user)


@pytest.mark.changes_db
async def test_remove_organization() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de"  # NOSONAR
    org_name = "tatsumi"
    email = "org_testuser1@gmail.com"
    modified_date = "2019-11-22T20:07:57+00:00"
    await orgs_domain.update_state(
        organization_id=org_id,
        organization_name=org_name,
        state=OrganizationState(
            modified_by=email,
            modified_date=modified_date,
            status=OrganizationStateStatus.DELETED,
            pending_deletion_date="",
        ),
    )

    loaders = get_new_context()
    org: Organization = await loaders.organization.load(org_id)
    assert org.state.status == OrganizationStateStatus.DELETED
    assert org.state.modified_by == email
    assert org.state.modified_date == modified_date
    assert org.state.pending_deletion_date is None


async def test_get_id_by_name() -> None:
    org_name = "okada"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(org_name)
    org_id = organization.id
    assert org_id == expected_org_id


async def test_get_name_by_id() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    expected_org_name = "okada"
    organization: Organization = await loaders.organization.load(org_id)
    org_name = organization.name
    assert org_name == expected_org_name


async def test_get_id_for_group() -> None:
    group_name = "unittesting"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load(group_name)
    org_id = group.organization_id
    assert org_id == expected_org_id

    with pytest.raises(GroupNotFound):
        await loaders.group.load("madeup-group")


async def test_get_stakeholder_organizations() -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder_email = "integratesmanager@gmail.com"
    expected_orgs = [
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",  # NOSONAR
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",  # NOSONAR
    ]
    stakeholder_orgs_access = (
        await loaders.stakeholder_organizations_access.load(stakeholder_email)
    )
    stakeholder_orgs_ids = [
        org.organization_id for org in stakeholder_orgs_access
    ]
    assert sorted(stakeholder_orgs_ids) == expected_orgs

    assert (
        await loaders.stakeholder_organizations_access.load(
            "madeupstakeholder@gmail.com"
        )
        == ()  # NOSONAR
    )


@pytest.mark.changes_db
async def test_remove_user() -> None:
    user = "org_testuser3@gmail.com"
    modified_by = "org_testadmin@gmail.com"
    group = "sheele"
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    loaders = get_new_context()
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group
    )
    assert user in group_users
    assert await authz.get_group_level_role(loaders, user, group) == "user"
    assert (
        await authz.get_organization_level_role(loaders, user, org_id)
        == "user"
    )

    await orgs_domain.remove_access(loaders, org_id, user, modified_by)
    loaders = get_new_context()
    updated_group_users = (
        await group_access_domain.get_group_stakeholders_emails(loaders, group)
    )
    assert user not in updated_group_users
    assert await authz.get_group_level_role(loaders, user, group) == ""
    assert await authz.get_organization_level_role(loaders, user, org_id) == ""

    with pytest.raises(StakeholderNotInOrganization):
        await orgs_domain.remove_access(
            loaders, org_id, "madeupuser@gmail.com", modified_by
        )


@pytest.mark.changes_db
async def test_update_policies() -> None:
    org_id = "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86"
    org_name = "bulat"
    email = "org_testuser1@gmail.com"
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(org_id)
    max_acceptance_days = organization.policies.max_acceptance_days
    max_acceptance_severity = organization.policies.max_acceptance_severity
    max_number_acceptances = organization.policies.max_number_acceptances
    min_acceptance_severity = organization.policies.min_acceptance_severity

    assert max_acceptance_days is None
    assert max_acceptance_severity == Decimal("6.9")
    assert max_number_acceptances is None
    assert min_acceptance_severity == Decimal("3.4")

    new_values = PoliciesToUpdate(
        max_acceptance_days=20,
        max_acceptance_severity=Decimal("8.3"),
        max_number_acceptances=3,
        min_acceptance_severity=Decimal("2.2"),
    )
    await orgs_domain.update_policies(
        get_new_context(), org_id, org_name, email, new_values
    )

    loaders = get_new_context()
    updated_org: Organization = await loaders.organization.load(org_id)
    max_acceptance_days = updated_org.policies.max_acceptance_days
    max_acceptance_severity = updated_org.policies.max_acceptance_severity
    max_number_acceptances = updated_org.policies.max_number_acceptances
    min_acceptance_severity = updated_org.policies.min_acceptance_severity

    assert max_acceptance_days == Decimal("20")
    assert max_acceptance_severity == Decimal("8.3")
    assert max_number_acceptances == Decimal("3")
    assert min_acceptance_severity == Decimal("2.2")

    new_values = PoliciesToUpdate(max_acceptance_days=-10)
    with pytest.raises(InvalidAcceptanceDays):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        max_acceptance_severity=Decimal("10.5"),
    )
    with pytest.raises(InvalidAcceptanceSeverity):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(max_number_acceptances=-1)
    with pytest.raises(InvalidNumberAcceptances):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        min_acceptance_severity=Decimal("-1.5"),
    )
    with pytest.raises(InvalidAcceptanceSeverity):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        max_acceptance_severity=Decimal("5.0"),
        min_acceptance_severity=Decimal("7.4"),
    )
    with pytest.raises(InvalidAcceptanceSeverityRange):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        min_breaking_severity=Decimal("10.5"),
    )
    with pytest.raises(InvalidSeverity):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )


async def test_validate_negative_values() -> None:
    with pytest.raises(InvalidAcceptanceSeverity):
        orgs_domain.validate_max_acceptance_severity(Decimal("-1"))

    with pytest.raises(InvalidAcceptanceSeverity):
        orgs_domain.validate_min_acceptance_severity(Decimal("-1"))

    with pytest.raises(InvalidAcceptanceDays):
        orgs_domain.validate_max_acceptance_days(-1)

    with pytest.raises(InvalidNumberAcceptances):
        orgs_domain.validate_max_number_acceptances(-1)

    with pytest.raises(InvalidSeverity):
        orgs_domain.validate_min_breaking_severity(-1)

    with pytest.raises(InvalidVulnerabilityGracePeriod):
        orgs_domain.validate_vulnerability_grace_period(-1)


async def test_validate_severity_range() -> None:
    with pytest.raises(InvalidAcceptanceSeverity):
        orgs_domain.validate_max_acceptance_severity(Decimal("10.1"))

    with pytest.raises(InvalidAcceptanceSeverity):
        orgs_domain.validate_min_acceptance_severity(Decimal("10.1"))

    values = PoliciesToUpdate(
        min_acceptance_severity=Decimal("8.0"),
        max_acceptance_severity=Decimal("5.0"),
    )
    with pytest.raises(InvalidAcceptanceSeverityRange):
        await orgs_domain.validate_acceptance_severity_range(
            get_new_context(),
            "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
            values,
        )

    with pytest.raises(InvalidAcceptanceSeverityRange):
        await group_domain.validate_acceptance_severity_range(
            loaders=get_new_context(),
            group_name="oneshottest",
            values=values,
        )


async def test_iterate_organizations() -> None:
    expected_organizations = {
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3": "okada",
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86": "bulat",
        "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2": "hajime",
        "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de": "tatsumi",
        "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2": "himura",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1": "makimachi",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac": "kamiya",
        "ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448": "kiba",
        "ORG#7376c5fe-4634-4053-9718-e14ecbda1e6b": "imamura",
        "ORG#d32674a9-9838-4337-b222-68c88bf54647": "makoto",
        "ORG#ed6f051c-2572-420f-bc11-476c4e71b4ee": "ikari",
    }
    async for organization in orgs_domain.iterate_organizations():
        assert expected_organizations.pop(organization.id) == organization.name
    assert expected_organizations == {}


async def test_iterate_organizations_and_groups() -> None:
    loaders: Dataloaders = get_new_context()
    expected_organizations_and_groups: dict[str, Any] = {
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3": {
            "okada": ["oneshottest", "continuoustesting", "unittesting"]
        },
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86": {"bulat": []},
        "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2": {
            "hajime": ["kurome", "sheele"]
        },
        "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de": {"tatsumi": ["lubbock"]},
        "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2": {"himura": []},
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1": {
            "makimachi": [
                "metropolis",
                "deletegroup",
                "gotham",
                "asgard",
                "setpendingdeletion",
            ]
        },
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac": {
            "kamiya": ["barranquilla", "monteria"]
        },
        "ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448": {"kiba": []},
        "ORG#7376c5fe-4634-4053-9718-e14ecbda1e6b": {
            "imamura": ["deleteimamura"]
        },
        "ORG#d32674a9-9838-4337-b222-68c88bf54647": {"makoto": []},
        "ORG#ed6f051c-2572-420f-bc11-476c4e71b4ee": {"ikari": []},
    }
    async for org_id, org_name, groups in iterate_organizations_and_groups(
        loaders
    ):  # noqa
        assert sorted(groups) == sorted(
            expected_organizations_and_groups.pop(org_id)[org_name]
        )
    assert expected_organizations_and_groups == {}


async def test_get_all_active_group() -> None:
    loaders: Dataloaders = get_new_context()
    test_data = await orgs_domain.get_all_active_group_names(loaders)
    expected_output = [
        "asgard",
        "barranquilla",
        "continuoustesting",
        "deletegroup",
        "deleteimamura",
        "gotham",
        "lubbock",
        "kurome",
        "metropolis",
        "monteria",
        "oneshottest",
        "setpendingdeletion",
        "sheele",
        "unittesting",
    ]
    assert sorted(list(test_data)) == sorted(expected_output)
