import pytest

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
    assert len(groups) == 1

    group_name = 'testgroup'
    await org_dal.add_group(org_id, group_name)
    groups = await org_dal.get_groups(org_id)
    assert len(groups) == 2
    assert sorted(groups) == ['norway', group_name]


@pytest.mark.changes_db
async def test_add_user():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    users = await org_dal.get_users(org_id)
    assert len(users) == 1

    email = 'test@testemail.com'
    await org_dal.add_user(org_id, email)
    users = await org_dal.get_users(org_id)
    assert len(users) == 2
    assert sorted(users) == ['integratesmanager@gmail.com', email]


@pytest.mark.changes_db
async def test_create():
    org_name = 'test-org-creating'
    new_org = await org_dal.create(org_name)
    assert isinstance(new_org, dict)
    assert 'id' in new_org
    assert new_org['name'] == org_name
    with pytest.raises(InvalidOrganization):
        await org_dal.create(org_name)

async def test_exists():
    existing_group = await org_dal.exists('testorg')
    assert existing_group
    non_existent_group = await org_dal.exists('no-exists')
    assert not non_existent_group

async def test_get():
    ex_org_name = 'testorg'
    not_ex_org_name = 'no-exists'
    existing_org = await org_dal.get(ex_org_name)
    assert isinstance(existing_org, dict)
    assert 'id' in existing_org
    assert existing_org['name'] == ex_org_name
    not_existent_org = await org_dal.get(not_ex_org_name)
    assert not not_existent_org


async def test_get_groups():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    groups = await org_dal.get_groups(org_id)
    assert len(groups) == 1
    assert groups[0] == 'norway'


async def test_organizations_by_id():
    org_ids = [
        'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3',
        'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    ]
    orgs = await org_dal.get_many_by_id(org_ids)
    assert len(orgs) == 2
    assert orgs[0]['name'] == 'testorg'
    assert orgs[1]['name'] == 'testorg2'


async def test_get_user_organization_ids():
    email = 'integratesmanager@gmail.com'
    org_ids = await org_dal.get_for_user(email)
    assert len(org_ids) == 2
    assert sorted(org_ids) == \
        [
            'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3',
            'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
        ]


async def test_get_users():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    users = await org_dal.get_users(org_id)
    assert len(users) == 1
    assert users[0] == 'integratesmanager@gmail.com'


@pytest.mark.changes_db
async def test_get_or_create():
    ex_org_name = 'testorg'
    not_ex_org_name = 'new-org'
    existing_org = await org_dal.get_or_create(ex_org_name)
    assert isinstance(existing_org, dict)
    assert existing_org['id'] == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    assert existing_org['name'] == ex_org_name

    not_existent_org = await org_dal.get_or_create(not_ex_org_name)
    assert isinstance(not_existent_org, dict)
    assert 'id' in not_existent_org
    assert not_existent_org['name'] == not_ex_org_name
