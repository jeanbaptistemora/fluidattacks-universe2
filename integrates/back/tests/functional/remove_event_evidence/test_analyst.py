# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_event_evidence')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    event: str = '418900980'
    query = f'''
        mutation {{
            removeEventEvidence(eventId: "{event}",
                                evidenceType: IMAGE) {{
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
    assert result['data']['removeEventEvidence']['success']
