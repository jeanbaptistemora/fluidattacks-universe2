import pytest
from decimal import Decimal

import backend.dal.organization as org_dal
from backend.exceptions import InvalidOrganization

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


def test__map_keys_to_domain():
    test_dict = {
        'pk': 'primary-key',
        'sk': 'secondary-key',
        'attr1': 'attribute_1',
        'attr2': 'attribute_2'
    }
    mapped_dict = org_dal._map_keys_to_domain(test_dict)
    assert mapped_dict['id'] == test_dict['pk']
    assert mapped_dict['name'] == test_dict['sk']
    assert mapped_dict['attr1'] == test_dict['attr1']
    assert mapped_dict['attr2'] == test_dict['attr2']
    assert 'pk' not in mapped_dict
    assert 'sk' not in mapped_dict


def test__map_keys_to_dal():
    test_dict = {
        'id': 'primary-key',
        'name': 'secondary-key',
        'attr1': 'attribute_1',
        'attr2': 'attribute_2'
    }
    mapped_dict = org_dal._map_keys_to_dal(test_dict)
    assert mapped_dict['pk'] == test_dict['id']
    assert mapped_dict['sk'] == test_dict['name']
    assert mapped_dict['attr1'] == test_dict['attr1']
    assert mapped_dict['attr2'] == test_dict['attr2']
    assert 'id' not in mapped_dict
    assert 'name' not in mapped_dict


def test__map_attributes_to_dal():
    test_list = ['id', 'name', 'attr1', 'attr2']
    mapped_list = org_dal._map_attributes_to_dal(test_list)
    assert 'pk' in mapped_list
    assert 'sk' in mapped_list
    assert 'attr1' in mapped_list
    assert 'attr2' in mapped_list
    assert 'id' not in mapped_list
    assert 'name' not in mapped_list


@pytest.mark.changes_db
async def test_add_group():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    groups = await org_dal.get_groups(org_id)

    group_name = 'mine'
    await org_dal.add_group(org_id, group_name)
    updated_groups = await org_dal.get_groups(org_id)
    assert len(updated_groups) == len(groups) + 1
    assert sorted(updated_groups) == sorted(groups + [group_name])


@pytest.mark.changes_db
async def test_add_user():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    users = await org_dal.get_users(org_id)

    email = 'org_testuser1@gmail.com'
    await org_dal.add_user(org_id, email)
    updated_users = await org_dal.get_users(org_id)
    assert len(updated_users) == len(users) + 1
    assert sorted(updated_users) == sorted(users + [email])


@pytest.mark.changes_db
async def test_create():
    org_name = 'test-create-org'
    new_org = await org_dal.create(org_name)
    assert isinstance(new_org, dict)
    assert 'id' in new_org
    assert new_org['name'] == org_name
    with pytest.raises(InvalidOrganization):
        await org_dal.create(org_name)


@pytest.mark.changes_db
async def test_delete():
    org_name = 'himura'
    assert await org_dal.exists(org_name)

    org = await org_dal.get_by_name(org_name, ['id'])
    await org_dal.delete(org['id'], org_name)
    assert not await org_dal.exists(org_name)


@pytest.mark.changes_db
async def test_remove_group():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    group = 'kurome'
    groups = await org_dal.get_groups(org_id)
    assert len(groups) > 0

    await org_dal.remove_group(org_id, group)
    updated_groups = await org_dal.get_groups(org_id)
    assert len(updated_groups) == len(groups) - 1


@pytest.mark.changes_db
async def test_remove_user():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    user = 'org_testuser2@gmail.com'
    users = await org_dal.get_users(org_id)
    assert len(users) > 0
    assert user in users

    await org_dal.remove_user(org_id, user)
    updated_users = await org_dal.get_users(org_id)
    assert len(updated_users) == len(users) - 1
    assert user not in updated_users


async def test_exists():
    existing_group = await org_dal.exists('okada')
    assert existing_group
    non_existent_group = await org_dal.exists('no-exists')
    assert not non_existent_group


async def test_get_by_id():
    ex_org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    not_ex_org_id = 'ORG#2395b997-c81a-4094-9dae-b171a7b5428c'
    existing_org = await org_dal.get_by_id(ex_org_id)
    assert isinstance(existing_org, dict)
    assert 'name' in existing_org
    assert existing_org['id'] == ex_org_id
    not_existent_org = await org_dal.get_by_id(not_ex_org_id)
    assert not not_existent_org


async def test_get_by_name():
    ex_org_name = 'okada'
    not_ex_org_name = 'no-exists'
    existing_org = await org_dal.get_by_name(ex_org_name)
    assert isinstance(existing_org, dict)
    assert 'id' in existing_org
    assert existing_org['name'] == ex_org_name
    not_existent_org = await org_dal.get_by_name(not_ex_org_name)
    assert not not_existent_org


async def test_get_many_by_id():
    org_ids = [
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3',
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86',
        'ORG#49bcf63c-cd96-442f-be79-aa51574dc187'  # does not exist
    ]
    orgs = await org_dal.get_many_by_id(org_ids, ['id', 'name'])
    assert orgs[0]['id'] == org_ids[0]
    assert orgs[1]['name'] == 'bulat'
    assert not orgs[2]


async def test_get_id_for_group():
    existing_group = 'unittesting'
    non_existent_group = 'madeup'
    org_id_1 = await org_dal.get_id_for_group(existing_group)
    org_id_2 = await org_dal.get_id_for_group(non_existent_group)
    assert org_id_1 == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    assert org_id_2 == ''


async def test_get_ids_for_user():
    existing_user = 'integratesmanager@gmail.com'
    non_existent_user = 'madeupuser@gmail.com'
    org_ids_1 = await org_dal.get_ids_for_user(existing_user)
    org_ids_2 = await org_dal.get_ids_for_user(non_existent_user)
    assert sorted(org_ids_1) == [
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3',
        'ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac',
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86',
        'ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1'
    ]
    assert org_ids_2 == []


async def test_get_groups():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    groups = await org_dal.get_groups(org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        'continuoustesting',
        'oneshottest',
        'unittesting'
    ]


async def test_get_users():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    users = await org_dal.get_users(org_id)
    assert len(users) == 8
    assert sorted(users) == [
        'continuoushack2@gmail.com',
        'continuoushacking@gmail.com',
        'integratesanalyst@fluidattacks.com',
        'integratescloser@gmail.com',
        'integratescustomer@gmail.com',
        'integratesmanager@gmail.com',
        'integratesuser@gmail.com',
        'unittest2@fluidattacks.com'
    ]


async def test_has_group():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    existing_group = 'unittesting'
    non_existent_group = 'madeupgroup'
    assert await org_dal.has_group(org_id, existing_group)
    assert not await org_dal.has_group(org_id, non_existent_group)


async def test_has_user_access():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    existing_user = 'integratesmanager@gmail.com'
    non_existent_user = 'madeupuser@gmail.com'
    assert await org_dal.has_user_access(org_id, existing_user)
    assert not await org_dal.has_user_access(org_id, non_existent_user)


@pytest.mark.changes_db
async def test_update():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    org_name = 'okada'
    org_details = await org_dal.get_by_id(org_id)
    assert org_details['max_acceptance_days'] == 60
    assert 'max_acceptance_severity' not in org_details
    assert org_details['max_number_acceptations'] == 2
    assert 'min_acceptance_severity' not in org_details

    new_values = {
        'max_acceptance_days': None,
        'max_acceptance_severity': Decimal('8.0'),
        'max_number_acceptations': 5,
        'min_acceptance_severity': Decimal('2.5')
    }
    await org_dal.update(org_id, org_name, new_values)
    org_details = await org_dal.get_by_id(org_id)
    assert 'max_acceptance_days' not in org_details
    assert org_details['max_acceptance_severity'] == Decimal('8.0')
    assert org_details['max_number_acceptations'] == 5
    assert org_details['min_acceptance_severity'] == Decimal('2.5')


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
    async for org_id, org_name in org_dal.iterate_organizations():
        assert expected_organizations.pop(org_id) == org_name
    assert expected_organizations == {}
