# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('edit_group')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    group: str = 'group1'
    query = f"""
        mutation {{
            editGroup(
                comments: "",
                groupName: "{group}",
                subscription: ONESHOT,
                hasDrills: false,
                hasForces: false,
                hasIntegrates: false,
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['editGroup']
    assert result['data']['editGroup']['success']
