# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('project')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'admin@gmail.com'
    group: str = 'group1'
    consult: str = 'This is a test comment'
    finding: str = '475041521'
    event: str = '418900971'
    root: str = 'ROOT#63298a73-9dff-46cf-b42d-9b2f01a56690'
    draft = {
        'id': '475041531',
        'title': 'FIN.H.060. Insecure exceptions',
    }
    stakeholders: str = [
        'admin@gmail.com',
        'analyst@gmail.com',
    ]
    query = f'''
        query {{
            project(projectName: "{group}"){{
                name
                hasDrills
                hasForces
                hasIntegrates
                openVulnerabilities
                closedVulnerabilities
                lastClosingVuln
                maxSeverity
                meanRemediate
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                openFindings
                totalFindings
                totalTreatment
                subscription
                deletionDate
                userDeletion
                tags
                description
                consulting {{
                    content
                }}
                findings(filters: {{affectedSystems: "system1", actor: "SOME_CUSTOMERS"}}) {{
                    id
                }}
                events {{
                    id
                }}
                roots {{
                    ...on GitRoot {{
                        id
                    }}
                }}
                drafts {{
                    id
                    title
                }}
                stakeholders {{
                    email
                }}
                __typename
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
    assert result['data']['project']['name'] == group
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['openVulnerabilities'] == 1
    assert result['data']['project']['closedVulnerabilities'] == 1
    assert result['data']['project']['lastClosingVuln'] == 40
    assert result['data']['project']['maxSeverity'] == 4.1
    assert result['data']['project']['meanRemediate'] == 2
    assert result['data']['project']['meanRemediateLowSeverity'] == 3
    assert result['data']['project']['meanRemediateMediumSeverity'] == 4
    assert result['data']['project']['openFindings'] == 1
    assert result['data']['project']['totalFindings'] == 1
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['tags'] == ['testing']
    assert result['data']['project']['description'] == 'this is group1'
    assert consult in [consult['content'] for consult in result['data']['project']['consulting']]
    assert finding in [finding['id'] for finding in result['data']['project']['findings']]
    assert event in [event['id'] for event in result['data']['project']['events']]
    assert root in [root['id'] for root in result['data']['project']['roots']]
    assert draft in result['data']['project']['drafts']
    assert stakeholders == sorted([stakeholder['email'] for stakeholder in result['data']['project']['stakeholders']])
