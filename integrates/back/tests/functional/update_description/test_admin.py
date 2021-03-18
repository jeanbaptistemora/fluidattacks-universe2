# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_finding_description')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'admin@gmail.com'
    finding_id: str = '475041513'
    actor: str = 'ANYONE_INTERNET'
    affected_systems: str = 'Server bWAPP'
    attack_vector_desc: str = 'This is an updated attack vector'
    records: str = 'Clave plana'
    records_number: int = 12
    cwe: str = '200'
    description: str = 'I just have updated the description'
    recommendation: str = 'Updated recommendation'
    requirements: str = 'REQ.0132. Passwords (phrase type) must be at least 3 words long.'
    scenario: str = 'UNAUTHORIZED_USER_EXTRANET'
    threat: str = 'Updated threat'
    title: str = 'F051. Weak passwords reversed'
    finding_type: str = 'SECURITY'
    query = f'''
        mutation {{
            updateDescription(
                actor: "{actor}",
                affectedSystems: "{affected_systems}",
                attackVectorDesc: "{attack_vector_desc}",
                cwe: "{cwe}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                recordsNumber: {records_number},
                requirements: "{requirements}",
                scenario: "{scenario}",
                threat: "{threat}",
                title: "{title}",
                findingType: "{finding_type}"
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
    assert 'success' in result['data']['updateDescription']
    assert result['data']['updateDescription']['success']
