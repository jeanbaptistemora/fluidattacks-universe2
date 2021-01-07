import json
import pytest

from test_async.functional_test.internal_manager.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_project():
    query = '''{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    group_name = result['data']['internalNames']['name']

    org_name = 'okada'
    query = f'''
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "This is a new project from pytest",
                projectName: "{group_name}",
                subscription: CONTINUOUS,
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                closedVulnerabilities
                consulting {{
                    content
                }}
                drafts {{
                    analyst
                }}
                deletionDate
                description
                events {{
                    analyst
                    detail
                }}
                findings {{
                    analyst
                }}
                hasDrills
                hasForces
                hasIntegrates
                lastClosingVuln
                lastClosingVulnFinding {{
                    analyst
                }}
                maxOpenSeverity
                maxOpenSeverityFinding {{
                    analyst
                }}
                maxSeverity
                maxSeverityFinding {{
                    analyst
                }}
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                name
                openFindings
                openVulnerabilities
                organization
                serviceAttributes
                stakeholders {{
                    email
                    firstLogin
                    lastLogin
                    phoneNumber
                    responsibility
                    role
                }}
                subscription
                tags
                totalFindings
                totalTreatment
                userDeletion
                userRole
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert result['data']['project']['closedVulnerabilities'] == 0
    assert result['data']['project']['consulting'] == []
    assert result['data']['project']['drafts'] == []
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['description'] == 'This is a new project from pytest'
    assert result['data']['project']['events'] == []
    assert result['data']['project']['findings'] == []
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['lastClosingVuln'] == 0
    assert result['data']['project']['lastClosingVulnFinding'] == None
    assert result['data']['project']['maxOpenSeverity'] == 0.0
    assert result['data']['project']['maxOpenSeverityFinding'] == None
    assert result['data']['project']['maxSeverity'] == 0.0
    assert result['data']['project']['maxSeverityFinding'] == None
    assert result['data']['project']['meanRemediate'] == 0
    assert result['data']['project']['meanRemediateCriticalSeverity'] == 0
    assert result['data']['project']['meanRemediateHighSeverity'] == 0
    assert result['data']['project']['meanRemediateLowSeverity'] == 0
    assert result['data']['project']['meanRemediateMediumSeverity'] == 0
    assert result['data']['project']['name'] == group_name
    assert result['data']['project']['openFindings'] == 0
    assert result['data']['project']['openVulnerabilities'] == 0
    assert result['data']['project']['organization'] == org_name
    assert result['data']['project']['serviceAttributes'] == [
        'has_drills_white',
        'is_fluidattacks_customer',
        'is_continuous',
        'has_integrates',
        'has_forces',
        'must_only_have_fluidattacks_hackers',
    ]
    assert len(result['data']['project']['stakeholders']) == 2
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['tags'] == []
    assert result['data']['project']['totalFindings'] == 0
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['userDeletion'] == ''
