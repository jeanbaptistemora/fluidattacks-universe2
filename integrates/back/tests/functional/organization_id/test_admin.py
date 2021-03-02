# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.organization_id
async def test_organization_id_admin(populate: bool):
    context = get_new_context()
    assert populate
    query = '''{
        organizationId(organizationName: "orgtest") {
            id
        }
    }'''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        'test1@test1.com',
        context=context
    )
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] != None
