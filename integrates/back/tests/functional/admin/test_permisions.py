import pytest

from back.tests.functional.admin.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_permissions():
    query = '''{
        groupsWithForces
    }'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['groupsWithForces'][0] == 'unittesting'
    result = await get_result(data, stakeholder='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
