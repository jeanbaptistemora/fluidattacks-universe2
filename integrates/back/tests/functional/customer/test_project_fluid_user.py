# Standard libraries
import json
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.customer.utils import get_result


@pytest.mark.asyncio
@pytest.mark.old
async def test_project_fluid_user():
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
        stakeholder='integratescustomer@fluidattacks.com',
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
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    context = get_new_context()
    role = 'CUSTOMER'
    customer_email = 'integratescustomer@fluidattacks.com'
    query = f'''
        mutation {{
            editStakeholder (
                email: "{customer_email}",
                phoneNumber: "-",
                projectName: "{group_name}",
                responsibility: "Customer",
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
    assert result['data']['editStakeholder']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            addProjectConsult(
                content: "Test consult",
                parent: "0",
                projectName: "{group_name}",
            ) {{
                success
                commentId
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
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
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert 'success' in result['data']['addTags']
    assert result['data']['addTags']['success']

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
                events {{
                    analyst
                    detail
                }}
                serviceAttributes
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert result['data']['project']['name'] == group_name
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['findings'] == []
    assert result['data']['project']['openVulnerabilities'] == 0
    assert result['data']['project']['closedVulnerabilities'] == 0
    assert result['data']['project']['lastClosingVuln'] == 0
    assert result['data']['project']['maxSeverity'] == 0.0
    assert result['data']['project']['meanRemediate'] == 0
    assert result['data']['project']['meanRemediateLowSeverity'] == 0
    assert result['data']['project']['meanRemediateMediumSeverity'] == 0
    assert result['data']['project']['openFindings'] == 0
    assert result['data']['project']['totalFindings'] == 0
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['tags'] == ['testing']
    assert result['data']['project']['description'] == 'This is a new project from pytest'
    assert result['data']['project']['consulting'] == [
        {'content': 'Test consult'}]
    assert result['data']['project']['events'] == []
    assert result['data']['project']['serviceAttributes'] == [
        'has_drills_white',
        'has_forces',
        'has_integrates',
        'is_continuous',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    ]
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
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert 'success' in result['data']['removeTag']
    assert result['data']['removeTag']['success']

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                tags
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert result['data']['project']['tags'] == []

    context = get_new_context()
    query = f'''
      mutation {{
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "{group_name}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/test2"
        ) {{
          success
        }}
      }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert result['data']['addGitRoot']['success']

    context = get_new_context()
    query = f'''
        query {{
          group: project(projectName: "{group_name}") {{
            roots {{
              __typename
              ...on GitRoot {{
                branch
                environment
                environmentUrls
                gitignore
                includesHealthCheck
                url
              }}
            }}
          }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' not in result
    assert {
        '__typename': 'GitRoot',
        'branch': 'master',
        'environment': 'production',
        'environmentUrls': [],
        'gitignore': [],
        'includesHealthCheck': True,
        'url': 'https://gitlab.com/fluidattacks/test2'
    } in result['data']['group']['roots']

    context = get_new_context()
    query = f'''
        mutation {{
            unsubscribeFromGroup(groupName: "{group_name}"){{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
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
    result = await get_result(
        data,
        stakeholder='integratescustomer@fluidattacks.com',
        context=context
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
