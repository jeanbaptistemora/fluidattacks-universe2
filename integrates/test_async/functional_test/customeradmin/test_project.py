import json
import pytest

from backend.domain.available_name import get_name
from backend.exceptions import (
    NotPendingDeletion,
    UserNotInOrganization
)
from test_async.functional_test.customeradmin.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_project():
    org_name = 'okada'
    group_name = await get_name('group')
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
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    group_name2 = await get_name('group')
    query = f'''
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "This is a new project from pytest",
                projectName: "{group_name2}",
                subscription: CONTINUOUS,
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    role = 'CUSTOMERADMIN'
    query = f'''
        mutation {{
            grantStakeholderAccess (
                email: "integratesuser@gmail.com",
                phoneNumber: "-",
                projectName: "{group_name}",
                responsibility: "Customer Admin",
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
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert  result['data']['grantStakeholderAccess']['success']

    query = f'''
        mutation {{
            grantStakeholderAccess (
                email: "integratesuser@gmail.com",
                phoneNumber: "-",
                projectName: "{group_name2}",
                responsibility: "Customer Admin",
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
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert  result['data']['grantStakeholderAccess']['success']

    query = f'''
        mutation {{
            removeGroup(
                groupName: "{group_name2}",
                subscription: CONTINUOUS
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['removeGroup']
    assert result['data']['removeGroup']['success']

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addTags']
    assert result['data']['addTags']['success']

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
                stakeholders {{
                    email
                    role
                }}
                serviceAttributes
                bill{{
                    developers{{
                        actor
                    }}
                }}
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
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
    assert result['data']['project']['consulting'] == [{'content': 'Test consult'}]
    assert result['data']['project']['events'] == []
    assert result['data']['project']['stakeholders'] ==  [
        {'email': 'unittest2@fluidattacks.com', 'role': 'group_manager'},
        {'email': 'integratesuser@gmail.com', 'role': 'customeradmin'},
    ]
    assert result['data']['project']['serviceAttributes'] == [
        'has_drills_white',
        'is_fluidattacks_customer',
        'has_integrates',
        'has_forces',
        'must_only_have_fluidattacks_hackers',
    ]
    assert result['data']['project']['bill']['developers'] == []

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['removeTag']
    assert result['data']['removeTag']['success']

    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                tags
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['project']['tags'] == []

    query = f'''
      mutation {{
        addGitRoot(
          branch: "master"
          environment: {{
            kind: "production"
            url: "https://integrates.fluidattacks.com"
          }}
          groupName: "{group_name}"
          url: "https://gitlab.com/fluidattacks/test3"
        ) {{
          success
        }}
      }}
    '''
    result = await get_result({'query': query})
    assert 'errors' not in result
    assert result['data']['addGitRoot']['success']

    query = f'''
        query {{
          group: project(projectName: "{group_name}") {{
            roots {{
              __typename
              ...on GitRoot {{
                branch
                directoryFiltering {{
                  paths
                  policy
                }}
                environment {{
                  kind
                  url
                }}
                url
              }}
            }}
          }}
        }}
    '''
    result = await get_result({'query': query})
    assert 'errors' not in result
    assert {
        '__typename': 'GitRoot',
        'branch': 'master',
        'directoryFiltering': None,
        'environment': {
            'kind': 'production',
            'url': 'https://integrates.fluidattacks.com'
        },
        'url': 'https://gitlab.com/fluidattacks/test3'
    } in result['data']['group']['roots']

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['editGroup']
    assert result['data']['editGroup']['success']

    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                hasDrills
                hasForces
                hasIntegrates
                subscription
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(UserNotInOrganization())
