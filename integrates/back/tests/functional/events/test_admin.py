# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('events')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'admin@gmail.com'
    group: str = 'group1'
    expected = [
        {
            'id': '418900971',
            'projectName': 'group1',
            'detail': 'Integrates unit test1',
        },
        {
            'id': '418900980',
            'projectName': 'group1',
            'detail': 'Integrates unit test2',
        },
    ]
    query = f'''{{
        events(projectName: "{group}"){{
            id
            projectName
            detail
        }}
    }}'''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    assert result['data']['events'] == expected
