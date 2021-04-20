import pytest

from groups.dal import get_attributes
from resources.dal import remove

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_remove():
    group_name = 'continuoustesting'

    group_info = await get_attributes(group_name, ['files'])
    files = group_info.get('files', [])

    assert await remove(group_name, 'files', 0)

    expected_group_info = await get_attributes(group_name, ['files'])
    expected_files = expected_group_info.get('files', [])

    assert expected_files == files[1:]
