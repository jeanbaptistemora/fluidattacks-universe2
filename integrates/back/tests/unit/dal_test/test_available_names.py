import pytest

from custom_exceptions import EmptyPoolName
from names import dal as names_dal


# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_remove():
    is_deleted = await names_dal.remove('manila', 'group')
    assert is_deleted


@pytest.mark.changes_db
async def test_empty_pool():
    all_groups = await names_dal.get_all('group')
    for group_name in all_groups:
        is_deleted = await names_dal.remove(group_name, 'group')
        assert is_deleted
    with pytest.raises(EmptyPoolName):
        assert await names_dal.get_one('group')

@pytest.mark.changes_db
async def test_create():
    is_created = await names_dal.create('manila', 'group')
    assert is_created

async def test_get_one():
    group_available = await names_dal.get_one('group')
    assert isinstance(group_available, str)

async def test_get_all():
    all_groups = await names_dal.get_all('group')
    assert isinstance(all_groups, list)
    assert len(all_groups) == 14

async def test_exists():
    existing_group = await names_dal.exists('praga', 'group')
    assert existing_group
    non_existent_group = await names_dal.exists('rio', 'group')
    assert not non_existent_group
