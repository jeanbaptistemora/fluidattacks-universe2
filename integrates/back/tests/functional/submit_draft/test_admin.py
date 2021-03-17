# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('submit_draft')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'admin@gmail.com'
    finding: str = '475041513'
    query = f'''
        mutation {{
            submitDraft(findingId: "{finding}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']
