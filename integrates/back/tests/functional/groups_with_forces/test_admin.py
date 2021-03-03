# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('groups_with_forces')
async def test_admin(populate: bool):
    context = get_new_context()
    assert populate
    user = 'test1@gmail.com'
    group_forces = 'group-2'
    group_not_forces = 'group-1'
    query = '''{
        groupsWithForces
    }'''

    # Get groups with forces
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    assert 'errors' not in result
    assert group_forces in result['data']['groupsWithForces']
    assert group_not_forces not in result['data']['groupsWithForces']

    # Try to get groups with non-existing user
    result = await get_graphql_result(
        data,
        stakeholder='madeupuser@gmail.com',
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
