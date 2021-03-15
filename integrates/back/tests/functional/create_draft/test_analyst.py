# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_draft')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    cwe: str = '200'
    description: str = 'This is pytest created draft'
    group_name: str = 'group1'
    recommendation: str = 'Solve this finding'
    requirements: str = 'REQ.0001. Apply filters'
    risk: str = 'This is pytest created draft'
    threat: str = 'Attacker'
    title: str = 'F001. Very serious vulnerability'
    draft_type: str = 'SECURITY'
    query = f'''
        mutation {{
            createDraft(
                cwe: "{cwe}",
                description: "{description}",
                projectName: "{group_name}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                risk: "{risk}",
                threat: "{threat}",
                title: "{title}",
                type: {draft_type}
            ) {{
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
    assert 'success' in result['data']['createDraft']
    assert result['data']['createDraft']['success']
