import json
import pytest

from back.tests.functional.service_forces.utils import get_result


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('old')
async def test_project():
    group_name = 'unittesting'

    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                name
                hasDrills
                hasForces
                findings {{
                    id
                }}
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
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['project']['closedVulnerabilities'] == 8
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['description'] == 'Integrates unit test project'
    assert len(result['data']['project']['findings']) == 9
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['lastClosingVuln'] == 23
    assert result['data']['project']['maxSeverity'] == 6.3
    assert result['data']['project']['meanRemediate'] == 245
    assert result['data']['project']['meanRemediateLowSeverity'] == 232
    assert result['data']['project']['meanRemediateMediumSeverity'] == 287
    assert result['data']['project']['name'] == group_name
    assert result['data']['project']['openFindings'] == 5
    assert result['data']['project']['openVulnerabilities'] == 31
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['tags'] == ['test-projects']
    assert result['data']['project']['totalFindings'] == 9
    assert result['data']['project']['totalTreatment'] == '{"accepted": 1, "inProgress": 4, "acceptedUndefined": 2, "undefined": 25}'
    assert result['data']['project']['userDeletion'] == ''
