# Third party libraries
import pytest

# Local libraries
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.organization_id
async def test_organization_id_admin(populate: bool):
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
    )
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] != None
