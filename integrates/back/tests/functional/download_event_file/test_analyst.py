# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_event_file')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    event: str = '418900971'
    query = f'''
        mutation {{
            downloadEventFile(
                eventId: "{event}",
                fileName: "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad"
            ) {{
                success
                url
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
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']
