import pytest
from decimal import Decimal

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
    InvalidOrganization
)
from backend.utils import aio

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
    groups_users = await aio.materialize(
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


async def test_get_id_for_group():
    group_name = 'unittesting'
    org_id = await org_domain.get_id_for_group(group_name)
    assert org_id == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'


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


async def test_get_max_number_acceptations():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    max_acceptations = await org_domain.get_max_number_acceptations(org_with_data)
    assert max_acceptations == Decimal('2')

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    max_acceptations = await org_domain.get_max_number_acceptations(org_without_data)
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
    ex_org_name = 'imamura'
    email = 'unittest@fluidattacks.com'
    not_ex_org_name = 'new-org'
    existing_org = await org_domain.get_or_create(ex_org_name, email)
    assert isinstance(existing_org, dict)
    assert existing_org['id'] == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'

    not_existent_org = await org_domain.get_or_create(not_ex_org_name, email)
    assert isinstance(not_existent_org, dict)
    assert not_existent_org


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
