# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)
from backend.exceptions import (
    InvalidOrganization,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_organization')
async def test_admin(populate: bool):
    context = get_new_context()
    assert populate
    org_name: str = 'TESTORG'
    query = f'''
        mutation {{
            createOrganization(name: "{org_name}") {{
                organization {{
                    id
                    name
                }}
                success
            }}
        }}
    '''

    # Create org
    data = {'query': query}
    result = await get_graphql_result(
        data,
        'test1@test1.com',
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['createOrganization']['success']
    assert result['data']['createOrganization']['organization']['name'] == org_name.lower()
    assert result['data']['createOrganization']['organization']['id'].startswith('ORG')

    # Try to create existing org
    data = {'query': query}
    result = await get_graphql_result(
        data,
        'test1@test1.com',
        context=context,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == InvalidOrganization().args[0]
