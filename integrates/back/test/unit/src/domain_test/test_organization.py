# pylint: disable=too-many-statements
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
    InvalidUserProvided,
    InvalidVulnerabilityGracePeriod,
    OrganizationNotFound,
    UserNotInOrganization,
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
    OrganizationPoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from graphql import (
    GraphQLError,
)
from group_access import (
    domain as group_access_domain,
)
from newutils import (
    organizations as orgs_utils,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from typing import (
    Any,
    Dict,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_group() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"  # NOSONAR
    group = "najenda"
    assert not await orgs_domain.has_group(org_id, group)

    await orgs_domain.add_group(org_id, group)
    assert await orgs_domain.has_group(org_id, group)

    users = await group_access_domain.get_group_users(group)
    assert (
        await authz.get_organization_level_role(users[0], org_id)
        == "customer_manager"
    )


@pytest.mark.changes_db
async def test_add_customer_manager_fail() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    user = "org_testgroupmanager2@gmail.com"
    assert not await orgs_domain.has_user_access(org_id, user)

    try:
        await orgs_domain.add_user(loaders, org_id, user, "customer_manager")
    except InvalidUserProvided as ex:
        assert str(ex) == (
            "Exception - This role can only be granted to Fluid Attacks "
            "users"
        )

    loaders = get_new_context()
    group_names = await orgs_domain.get_group_names(loaders, org_id)
    groups_users = await collect(
        group_access_domain.get_group_users(group) for group in group_names
    )
    assert all(user not in group_users for group_users in groups_users)


@pytest.mark.changes_db
async def test_add_customer_manager_good() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    user = "org_testgroupmanager2@fluidattacks.com"
    assert not await orgs_domain.has_user_access(org_id, user)

    assert await orgs_domain.add_user(
        loaders, org_id, user, "customer_manager"
    )
    assert (
        await authz.get_organization_level_role(user, org_id)
        == "customer_manager"
    )

    loaders = get_new_context()
    group_names = await orgs_domain.get_group_names(loaders, org_id)
    groups_users = await collect(
        group_access_domain.get_group_users(group) for group in group_names
    )
    assert all(user in group_users for group_users in groups_users)


@pytest.mark.changes_db
async def test_add_organization() -> None:
    loaders: Dataloaders = get_new_context()
    org_name = "esdeath"
    user = "org_testusermanager1@gmail.com"
    with pytest.raises(OrganizationNotFound):
        await loaders.organization.load(org_name)

    await orgs_domain.add_organization_typed(loaders, org_name, user)

    organization: Organization = await loaders.organization.load(org_name)
    org_id = organization.id
    assert await orgs_domain.has_user_access(org_id, user)
    assert (
        await authz.get_organization_level_role(user, org_id) == "user_manager"
    )

    with pytest.raises(InvalidOrganization):
        await orgs_domain.add_organization_typed(loaders, org_name, user)


@pytest.mark.changes_db
async def test_remove_organization() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de"  # NOSONAR
    email = "org_testuser1@gmail.com"
    await orgs_domain.update_org_state(
        loaders, org_id, email, OrganizationStateStatus.DELETED
    )

    new_loaders: Dataloaders = get_new_context()
    org: Organization = await new_loaders.organization.load(org_id)
    assert orgs_utils.is_deleted_typed(org)


async def test_get_groups() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"  # NOSONAR
    groups = await orgs_domain.get_groups(org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        "continuoustesting",
        "oneshottest",
        "unittesting",
    ]


async def test_get_id_by_name() -> None:
    org_name = "okada"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(org_name)
    org_id = organization.id
    assert org_id == expected_org_id

    with pytest.raises(OrganizationNotFound):
        new_loader: Dataloaders = get_new_context()
        await new_loader.organization.load("madeup-org")


async def test_get_name_by_id() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    expected_org_name = "okada"
    organization: Organization = await loaders.organization.load(org_id)
    org_name = organization.name
    assert org_name == expected_org_name

    with pytest.raises(OrganizationNotFound):
        new_loader: Dataloaders = get_new_context()
        new_organization: Organization = await new_loader.organization.load(
            "ORG#madeup-id"
        )
        org_name = new_organization.name


async def test_get_id_for_group() -> None:
    group_name = "unittesting"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load(group_name)
    org_id = group.organization_id
    assert org_id == expected_org_id

    with pytest.raises(GroupNotFound):
        await loaders.group.load("madeup-group")


@pytest.mark.changes_db
async def test_get_or_create() -> None:
    loaders: Dataloaders = get_new_context()
    ex_org_name = "okada"
    email = "unittest@fluidattacks.com"
    not_ex_org_name = "neworg"
    existing_org = await orgs_domain.get_or_add(loaders, ex_org_name, email)
    assert isinstance(existing_org, Organization)
    assert existing_org.id == "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    not_existent_org = await orgs_domain.get_or_add(
        loaders, not_ex_org_name, email
    )
    assert not_existent_org


async def test_get_user_organizations() -> None:
    user = "integratesmanager@gmail.com"
    expected_orgs = [
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",  # NOSONAR
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",  # NOSONAR
    ]
    user_orgs = await orgs_domain.get_user_organizations(user)
    assert sorted(user_orgs) == expected_orgs

    assert (
        await orgs_domain.get_user_organizations("madeupuser@gmail.com")
        == []  # NOSONAR
    )


async def test_get_users() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    users = await orgs_domain.get_users(org_id)
    expected = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "customer_manager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integratesexecutive@gmail.com",
        "integrateshacker@fluidattacks.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@gmail.com",
        "integratesuser@gmail.com",
        "unittest2@fluidattacks.com",
        "vulnmanager@gmail.com",
    ]
    assert len(users) == 18
    for user in expected:
        assert user in users


async def test_has_group() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_group = "unittesting"
    non_existent_group = "madeupgroup"
    assert await orgs_domain.has_group(org_id, existing_group)
    assert not await orgs_domain.has_group(org_id, non_existent_group)


async def test_has_user_access() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    assert await orgs_domain.has_user_access(org_id, existing_user)
    assert not await orgs_domain.has_user_access(org_id, non_existent_user)


@pytest.mark.changes_db
async def test_remove_user() -> None:
    user = "org_testuser3@gmail.com"
    group = "sheele"
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    group_users = await group_access_domain.get_group_users(group)
    assert user in group_users
    assert await authz.get_group_level_role(user, group) == "user"
    assert await authz.get_organization_level_role(user, org_id) == "user"

    assert await orgs_domain.remove_user(get_new_context(), org_id, user)
    updated_group_users = await group_access_domain.get_group_users(group)
    assert user not in updated_group_users
    assert await authz.get_group_level_role(user, group) == ""
    assert await authz.get_organization_level_role(user, org_id) == ""

    with pytest.raises(UserNotInOrganization):
        await orgs_domain.remove_user(
            get_new_context(), org_id, "madeupuser@gmail.com"
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

    new_values = OrganizationPoliciesToUpdate(
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

    new_values = OrganizationPoliciesToUpdate(max_acceptance_days=-10)
    exe = InvalidAcceptanceDays()
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = OrganizationPoliciesToUpdate(
        max_acceptance_severity=Decimal("10.5"),
    )
    exe = InvalidAcceptanceSeverity()
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = OrganizationPoliciesToUpdate(max_number_acceptances=-1)
    exe = InvalidNumberAcceptances()
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value
    new_values = OrganizationPoliciesToUpdate(
        min_acceptance_severity=Decimal("-1.5"),
    )
    exe = InvalidAcceptanceSeverity()
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = OrganizationPoliciesToUpdate(
        max_acceptance_severity=Decimal("5.0"),
        min_acceptance_severity=Decimal("7.4"),
    )
    exe = InvalidAcceptanceSeverityRange()
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = OrganizationPoliciesToUpdate(
        min_breaking_severity=Decimal("10.5"),
    )
    exe = InvalidSeverity([0.0, 10.0])
    with pytest.raises(GraphQLError) as excinfo:
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )
    assert GraphQLError(exe.args[0]) == excinfo.value


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

    values = OrganizationPoliciesToUpdate(
        min_acceptance_severity=Decimal("8.0"),
        max_acceptance_severity=Decimal("5.0"),
    )
    with pytest.raises(InvalidAcceptanceSeverityRange):
        await orgs_domain.validate_acceptance_severity_range_typed(
            get_new_context(),
            "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
            values,
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
    async for org_id, org_name in orgs_domain.iterate_organizations():
        assert expected_organizations.pop(org_id) == org_name
    assert expected_organizations == {}


async def test_iterate_organizations_and_groups() -> None:
    expected_organizations_and_groups: Dict[str, Any] = {
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
    async for org_id, org_name, groups in orgs_domain.iterate_organizations_and_groups():  # noqa
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
