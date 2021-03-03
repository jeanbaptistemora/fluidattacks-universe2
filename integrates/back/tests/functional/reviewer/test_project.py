# Standard libraries
import json
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import complete_register
from back.tests.functional.reviewer.utils import get_result


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
    result = await get_result(
        data,
        stakeholder='integratesmanager@gmail.com',
        context=context
    )
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    group_name = result['data']['internalNames']['name']

    context = get_new_context()
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
    result = await get_result(
        data,
        stakeholder='integratesmanager@gmail.com',
        context=context
    )
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    context = get_new_context()
    role = 'REVIEWER'
    reviewer_email = 'integratesreviewer@fluidattacks.com'
    query = f'''
        mutation {{
            grantStakeholderAccess (
                email: "{reviewer_email}",
                phoneNumber: "-",
                projectName: "{group_name}",
                responsibility: "Resourcer",
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
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
    assert  result['data']['grantStakeholderAccess']['success']
    assert await complete_register(reviewer_email, group_name)

    context = get_new_context()
    consult_content = 'Test reviewer consult'
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
    query = '''
        mutation AddTagsMutation($projectName: String!, $tagsData: JSONString!) {
            addTags (
                tags: $tagsData,
                projectName: $projectName) {
                success
            }
        }
    '''
    variables = {
        'projectName': group_name,
        'tagsData': json.dumps(['testing'])
    }
    data = {'query': query, 'variables': variables}
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
    query = f'''
        mutation {{
            removeTag (
                tag: "testing",
                projectName: "{group_name}",
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
    query = f"""
        mutation {{
            editGroup(
                comments: "",
                groupName: "{group_name}",
                subscription: ONESHOT,
                hasDrills: false,
                hasForces: false,
                hasIntegrates: false,
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                analytics(documentName: "", documentType: "")
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
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Exception - Document not found'
    assert result['data']['project']['closedVulnerabilities'] == 0
    assert result['data']['project']['consulting'] == [{'content': consult_content}]
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
        'has_forces',
        'has_integrates',
        'is_continuous',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    ]
    assert len(result['data']['project']['stakeholders']) == 3
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['tags'] == []
    assert result['data']['project']['totalFindings'] == 0
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['userRole'] == role.lower()

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
