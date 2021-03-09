# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('internal_names')
async def test_admin(populate: bool):
    assert populate
    group: str = 'group1'
    admin: str = 'test1@gmail.com'
    context = get_new_context()
    query = '''{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }'''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    assert result['data']['internalNames']['name'] == group
