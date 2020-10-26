import pytest
from decimal import Decimal

from aioextensions import collect
from graphql import GraphQLError

from backend import authz
from backend.domain import (
    organization as org_domain,
    project as project_domain
)
from backend.exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations,
    InvalidOrganization,
    UserNotInOrganization
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_group():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    group = 'najenda'
    assert not await org_domain.has_group(org_id, group)

    await org_domain.add_group(org_id, group)
    assert await org_domain.has_group(org_id, group)

    users = await project_domain.get_users(group)
    assert await authz.get_organization_level_role(
        users[0], org_id
    ) == 'group_manager'


@pytest.mark.changes_db
async def test_add_user():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    user = 'org_testgroupmanager2@gmail.com'
    assert not await org_domain.has_user_access(org_id, user)

    await org_domain.add_user(org_id, user, 'group_manager')
    assert await authz.get_organization_level_role(
        user, org_id
    ) == 'group_manager'

    groups = await org_domain.get_groups(org_id)
    groups_users = await collect(
        project_domain.get_users(group) for group in groups
    )
    assert all([user in group_users for group_users in groups_users])


@pytest.mark.changes_db
async def test_create_organization():
    org_name = 'esdeath'
    user = 'org_testusermanager1@gmail.com'
    with pytest.raises(InvalidOrganization):
        await org_domain.get_id_by_name(org_name)

    await org_domain.create_organization(org_name, user)
    org_id = await org_domain.get_id_by_name(org_name)
    assert await org_domain.has_user_access(org_id, user)
    assert await authz.get_organization_level_role(
        user, org_id
    ) == 'customeradmin'

    with pytest.raises(InvalidOrganization):
        await org_domain.create_organization(org_name, user)


@pytest.mark.changes_db
async def test_delete_organization():
    org_id = 'ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de'
    users = await org_domain.get_users(org_id)
    assert len(users) > 0

    await org_domain.delete_organization(org_id)
    updated_users = await org_domain.get_users(org_id)
    assert len(updated_users) == 0

    with pytest.raises(InvalidOrganization):
        await org_domain.get_name_by_id(org_id)


async def test_get_groups():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    groups = await org_domain.get_groups(org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        'continuoustesting',
        'oneshottest',
        'unittesting'
    ]


async def test_get_id_by_name():
    org_name = 'okada'
    expected_org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    org_id = await org_domain.get_id_by_name(org_name)
    assert org_id == expected_org_id

    with pytest.raises(InvalidOrganization):
        await org_domain.get_id_by_name('madeup-org')


async def test_get_name_by_id():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    expected_org_name = 'okada'
    org_name = await org_domain.get_name_by_id(org_id)
    assert org_name == expected_org_name

    with pytest.raises(InvalidOrganization):
        await org_domain.get_name_by_id('ORG#madeup-id')


async def test_get_id_for_group():
    group_name = 'unittesting'
    expected_org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    org_id = await org_domain.get_id_for_group(group_name)
    assert org_id == expected_org_id

    assert await org_domain.get_id_for_group('madeup-group') == ''


async def test_get_max_acceptance_days():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    days = await org_domain.get_max_acceptance_days(org_with_data)
    assert days == Decimal('60')

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    days = await org_domain.get_max_acceptance_days(org_without_data)
    assert days is None


async def test_get_max_acceptance_severity():
    org_with_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    max_severity = await org_domain.get_max_acceptance_severity(org_with_data)
    assert max_severity == Decimal('6.9')

    org_without_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    max_severity = await org_domain.get_max_acceptance_severity(org_without_data)
    assert max_severity == Decimal('10.0')


async def test_get_historic_max_number_acceptations():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    historic_max_acceptations = await org_domain.get_historic_max_number_acceptations(org_with_data)
    expected_max_acceptations = [{
        'date': '2019-11-22 15:07:57',
        'user': 'integratesmanager@gmail.com',
        'max_number_acceptations': Decimal('2'),
    }]
    assert historic_max_acceptations == expected_max_acceptations

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    historic_max_acceptations = await org_domain.get_historic_max_number_acceptations(org_without_data)
    assert historic_max_acceptations == []


async def test_get_current_max_number_acceptations_info():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    current_max_number_acceptations_info = (
        await org_domain.get_current_max_number_acceptations_info(
            org_with_data
        )
    )
    max_acceptations = (
        current_max_number_acceptations_info.get('max_number_acceptations')
    )
    assert max_acceptations == Decimal('2')

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    current_max_number_acceptations_info = (
        await org_domain.get_current_max_number_acceptations_info(
            org_without_data
        )
    )
    max_acceptations = (
        current_max_number_acceptations_info.get('max_number_acceptations')
    )
    assert max_acceptations is None


async def test_get_min_acceptance_severity():
    org_with_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    min_severity = await org_domain.get_min_acceptance_severity(org_with_data)
    assert min_severity == Decimal('3.4')

    org_without_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    min_severity = await org_domain.get_min_acceptance_severity(org_without_data)
    assert min_severity == Decimal('0.0')


@pytest.mark.changes_db
async def test_get_or_create():
    ex_org_name = 'okada'
    email = 'unittest@fluidattacks.com'
    not_ex_org_name = 'new-org'
    existing_org = await org_domain.get_or_create(ex_org_name, email)
    assert isinstance(existing_org, dict)
    assert existing_org['id'] == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'

    not_existent_org = await org_domain.get_or_create(not_ex_org_name, email)
    assert isinstance(not_existent_org, dict)
    assert not_existent_org


async def test_get_user_organizations():
    user = 'integratesmanager@gmail.com'
    expected_orgs = [
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3',
        'ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac',
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86',
        'ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1'
    ]
    user_orgs = await org_domain.get_user_organizations(user)
    assert sorted(user_orgs) == expected_orgs

    assert (
        await org_domain.get_user_organizations('madeupuser@gmail.com') == []
    )


async def test_get_uers():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    users = await org_domain.get_users(org_id)
    assert len(users) == 10
    assert sorted(users) == [
        'continuoushack2@gmail.com',
        'continuoushacking@gmail.com',
        'integratesanalyst@fluidattacks.com',
        'integratescloser@fluidattacks.com',
        'integratescustomer@gmail.com',
        'integratesexecutive@gmail.com',
        'integratesmanager@gmail.com',
        'integratesresourcer@gmail.com',
        'integratesuser@gmail.com',
        'unittest2@fluidattacks.com'
    ]


async def test_has_group():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    existing_group = 'unittesting'
    non_existent_group = 'madeupgroup'
    assert await org_domain.has_group(org_id, existing_group)
    assert not await org_domain.has_group(org_id, non_existent_group)


async def test_has_user_access():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    existing_user = 'integratesmanager@gmail.com'
    non_existent_user = 'madeupuser@gmail.com'
    assert await org_domain.has_user_access(org_id, existing_user)
    assert not await org_domain.has_user_access(org_id, non_existent_user)


@pytest.mark.changes_db
async def test_remove_user():
    user = 'org_testuser3@gmail.com'
    group = 'sheele'
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    group_users = await project_domain.get_users(group)
    assert user in group_users
    assert await authz.get_group_level_role(user, group) == 'customer'
    assert await authz.get_organization_level_role(user, org_id) == 'customer'

    assert await org_domain.remove_user(org_id, user)
    updated_group_users = await project_domain.get_users(group)
    assert user not in updated_group_users
    assert await authz.get_group_level_role(user, group) == ''
    assert await authz.get_organization_level_role(user, org_id) == ''

    with pytest.raises(UserNotInOrganization):
        await org_domain.remove_user(org_id, 'madeupuser@gmail.com')


@pytest.mark.changes_db
async def test_update_policies():
    org_id = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    org_name = 'bulat'
    current_max_number_acceptations_info = (
        await org_domain.get_current_max_number_acceptations_info(
            org_id
        )
    )
    max_acceptance_days = await org_domain.get_max_acceptance_days(org_id)
    max_acceptance_severity = await org_domain.get_max_acceptance_severity(org_id)
    max_number_acceptations = (
        current_max_number_acceptations_info.get('max_number_acceptations')
    )
    min_acceptance_severity = await org_domain.get_min_acceptance_severity(org_id)

    assert max_acceptance_days is None
    assert max_acceptance_severity == Decimal('6.9')
    assert max_number_acceptations is None
    assert min_acceptance_severity == Decimal('3.4')

    new_values = {
        'max_acceptance_days': '20',
        'max_acceptance_severity': '8.3',
        'max_number_acceptations': '3',
        'min_acceptance_severity': '2.2'
    }
    await org_domain.update_policies(org_id, org_name, '', new_values)

    current_max_number_acceptations_info = (
        await org_domain.get_current_max_number_acceptations_info(
            org_id
        )
    )
    max_acceptance_days = await org_domain.get_max_acceptance_days(org_id)
    max_acceptance_severity = await org_domain.get_max_acceptance_severity(org_id)
    max_number_acceptations = (
        current_max_number_acceptations_info.get('max_number_acceptations')
    )
    min_acceptance_severity = await org_domain.get_min_acceptance_severity(org_id)

    assert max_acceptance_days == Decimal('20')
    assert max_acceptance_severity == Decimal('8.3')
    assert max_number_acceptations == Decimal('3')
    assert min_acceptance_severity == Decimal('2.2')

    new_values = {'max_acceptance_days': '-10'}
    exe = InvalidAcceptanceDays()
    with pytest.raises(GraphQLError) as excinfo:
        await org_domain.update_policies(org_id, org_name, '', new_values)
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = {'max_acceptance_severity': '10.5'}
    exe = InvalidAcceptanceSeverity()
    with pytest.raises(GraphQLError) as excinfo:
        await org_domain.update_policies(org_id, org_name, '', new_values)
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = {'max_number_acceptations': '-1'}
    exe = InvalidNumberAcceptations()
    with pytest.raises(GraphQLError) as excinfo:
        await org_domain.update_policies(org_id, org_name, '', new_values)
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = {'min_acceptance_severity': '-1.5'}
    exe = InvalidAcceptanceSeverity()
    with pytest.raises(GraphQLError) as excinfo:
        await org_domain.update_policies(org_id, org_name, '', new_values)
    assert GraphQLError(exe.args[0]) == excinfo.value

    new_values = {
        'max_acceptance_severity': '5.0',
        'min_acceptance_severity': '7.4'
    }
    exe = InvalidAcceptanceSeverityRange()
    with pytest.raises(GraphQLError) as excinfo:
        await org_domain.update_policies(org_id, org_name, '', new_values)
    assert GraphQLError(exe.args[0]) == excinfo.value


async def test_validate_negative_values():
    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_max_acceptance_severity(Decimal('-1'))

    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_min_acceptance_severity(Decimal('-1'))

    with pytest.raises(InvalidAcceptanceDays):
        org_domain.validate_max_acceptance_days(-1)

    with pytest.raises(InvalidNumberAcceptations):
        org_domain.validate_max_number_acceptations(-1)


async def test_validate_severity_range():
    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_max_acceptance_severity(Decimal('10.1'))

    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_min_acceptance_severity(Decimal('10.1'))

    values = {
        'min_acceptance_severity': Decimal('8.0'),
        'max_acceptance_severity': Decimal('5.0')
    }
    with pytest.raises(InvalidAcceptanceSeverityRange):
        await org_domain.validate_acceptance_severity_range("", values)


async def test_iterate_organizations():
    expected_organizations = {
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3': 'okada',
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86': 'bulat',
        'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2': 'hajime',
        'ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de': 'tatsumi',
        'ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2': 'himura',
        'ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1': 'makimachi',
        'ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac': 'kamiya'
    }
    async for org_id, org_name in org_domain.iterate_organizations():
        assert expected_organizations.pop(org_id) == org_name
    assert expected_organizations == {}


async def test_iterate_organizations_and_groups():
    expected_organizations_and_groups = {
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3': {
            'okada': ['oneshottest', 'continuoustesting', 'unittesting']
        },
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86': {
            'bulat': ['pendingproject']
        },
        'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2': {
            'hajime': ['kurome', 'sheele']
        },
        'ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de': {
            'tatsumi': ['lubbock']
        },
        'ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2': {
            'himura': []
        },
        'ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1': {
            'makimachi': ['metropolis', 'gotham', 'asgard']
        },
        'ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac': {
            'kamiya': ['barranquilla', 'monteria']
        }
    }
    async for org_id, org_name, groups in org_domain.iterate_organizations_and_groups():
        assert sorted(groups) == sorted(expected_organizations_and_groups.pop(org_id)[org_name])
    assert expected_organizations_and_groups == {}
