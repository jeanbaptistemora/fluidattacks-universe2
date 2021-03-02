# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.analyst.utils import get_result


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('old')
async def test_project():
    context = get_new_context()
    query = '''{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }'''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    group_name = result['data']['internalNames']['name']

    context = get_new_context()
    org_name = 'okada'
    description = 'This is a new project from pytest'
    subscription = 'CONTINUOUS'
    query = f'''
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "{description}",
                projectName: "{group_name}",
                subscription: {subscription},
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    context = get_new_context()
    role = 'ANALYST'
    analyst_email = "integratesanalyst@fluidattacks.com"
    query = f'''
        mutation {{
            editStakeholder (
                email: "{analyst_email}",
                phoneNumber: "-",
                projectName: "{group_name}",
                responsibility: "Analyst",
                role: {role}
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratesmanager@gmail.com',
        context=context
    )
    assert 'errors' not in result
    assert  result['data']['editStakeholder']['success']

    context = get_new_context()
    consult_content = 'Test consult'
    query = f'''
        mutation {{
            addProjectConsult(
                content: "{consult_content}",
                parent: "0",
                projectName: "{group_name}",
            ) {{
                success
                commentId
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                name
                hasDrills
                hasForces
                findings {{
                    analyst
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
                consulting {{
                    content
                }}
                drafts {{
                    age
                }}
                events {{
                    analyst
                    detail
                }}
                serviceAttributes
                organization
                lastClosingVulnFinding{{
                    id
                }}
                maxSeverityFinding{{
                    id
                }}
                maxOpenSeverity
                maxOpenSeverityFinding{{
                    id
                }}
                meanRemediateHighSeverity
                meanRemediateCriticalSeverity
                serviceAttributes
                userRole
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['project']['name'] == group_name
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['findings'] == []
    assert result['data']['project']['openVulnerabilities'] == 0
    assert result['data']['project']['closedVulnerabilities'] == 0
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
    assert result['data']['project']['openFindings'] == 0
    assert result['data']['project']['totalFindings'] == 0
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['subscription'] == subscription.lower()
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['tags'] == []
    assert result['data']['project']['description'] == description
    assert result['data']['project']['consulting'] == [{'content': consult_content}]
    assert result['data']['project']['drafts'] == []
    assert result['data']['project']['events'] == []
    assert result['data']['project']['serviceAttributes'] == [
        'has_drills_white',
        'has_forces',
        'has_integrates',
        'is_continuous',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    ]
    assert result['data']['project']['organization'] == org_name
    assert result['data']['project']['userRole'] == role.lower()

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                findings(filters: {{affectedSystems: "test", actor: "ANY_EMPLOYEE"}}) {{
                id
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['project']['findings'] == []

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                findings(filters: {{affectedSystems: "notexists"}}) {{
                    id
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['project']['findings'] == []

    context = get_new_context()
    query = f'''
        mutation {{
            unsubscribeFromGroup(groupName: "{group_name}"){{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['unsubscribeFromGroup']['success']

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                name
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
