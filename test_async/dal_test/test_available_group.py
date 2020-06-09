import pytest

import backend.dal.available_group as available_group_dal
from backend.exceptions import EmptyPoolGroupName

@pytest.mark.changes_db
async def test_remove():
    is_deleted = await available_group_dal.remove('manila')
    assert is_deleted


@pytest.mark.changes_db
async def test_empty_pool():
    all_groups = await available_group_dal.get_all()
    for group_name in all_groups:
        is_deleted = await available_group_dal.remove(group_name)
        assert is_deleted
    with pytest.raises(EmptyPoolGroupName):
        assert await available_group_dal.get_one()

@pytest.mark.changes_db
async def test_create():
    is_created = await available_group_dal.create('manila')
    assert is_created

async def test_get_one():
    group_available = await available_group_dal.get_one()
    assert isinstance(group_available, str)

async def test_get_all():
    all_groups = await available_group_dal.get_all()
    assert isinstance(all_groups, list)
    assert len(all_groups) == 5

async def test_exists():
    existing_group = await available_group_dal.exists('praga')
    assert existing_group
    non_existent_group = await available_group_dal.exists('rio')
    assert not non_existent_group
