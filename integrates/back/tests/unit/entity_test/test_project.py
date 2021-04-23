# Standard libraries
from typing import (
    Any,
    Dict
)
import json

# Third party libraries
import pytest
from ariadne import graphql

# Local libraries
from back.tests.unit.utils import create_dummy_session
from backend.api import apply_context_attrs
from backend.api.schema import SCHEMA
from names.domain import get_name


pytestmark = pytest.mark.asyncio


async def _get_result_async(
  data: Dict[str, Any],
  user: str = 'integratesmanager@gmail.com'
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=user)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


async def test_project():
    """Check for project mutation."""
    variables = {
        'projectName': 'unittesting'
    }
    query = '''
      query GetProjectInfo($projectName: String!) {
        project(projectName: $projectName){
          name
          hasDrills
          hasForces
          findings {
              analyst
          }
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
          consulting {
            content
          }
          drafts {
            age
            openVulnerabilities
          }
          events {
            analyst
            detail
          }
          stakeholders {
            email
            invitationState
            role
            responsibility
            phoneNumber
            firstLogin
            lastLogin
          }
          __typename
        }
      }
    '''

    data = {'query': query, 'variables': variables}
    result = await _get_result_async(data)

    assert 'errors' not in result
    assert result['data']['project']['name'] == 'unittesting'
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert len(result['data']['project']['findings']) == 6
    assert result['data']['project']['openVulnerabilities'] == 31
    assert result['data']['project']['closedVulnerabilities'] == 8
    assert 'lastClosingVuln' in result['data']['project']
    assert result['data']['project']['maxSeverity'] == 6.3
    assert result['data']['project']['meanRemediate'] == 245
    assert result['data']['project']['meanRemediateLowSeverity'] == 232
    assert result['data']['project']['meanRemediateMediumSeverity'] == 287
    assert result['data']['project']['openFindings'] == 5
    assert result['data']['project']['totalFindings'] == 6
    assert 'totalTreatment' in result['data']['project']
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['tags'][0] == 'test-projects'
    assert result['data']['project']['description'] == 'Integrates unit test project'
    assert len(result['data']['project']['drafts']) == 1
    assert result['data']['project']['drafts'][0]['openVulnerabilities'] == 0
    assert len(result['data']['project']['events']) == 5
    assert result['data']['project']['consulting'][0]['content'] == 'Now we can post comments on projects'
    assert result['data']['project']['stakeholders'] == [
      {
          "email": "integratesserviceforces@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-10-29 13:40:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "service_forces",
      },
      {
          "email": "integratesmanager@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-12-29 11:50:17",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "admin",
      },
      {
          "email": "unittest2@fluidattacks.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-10-29 13:40:37",
          "phoneNumber": "-",
          "responsibility": "Tester",
          "role": "group_manager",
      },
      {
          "email": "integratesexecutive@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-10-29 13:40:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "executive",
      },
      {
          "email": "integratescustomer@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-10-29 13:40:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "customer",
      },
      {
          "email": "integratesuser@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2019-10-29 13:40:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "customeradmin",
      },
      {
          "email": "continuoushacking@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2020-03-23 10:45:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "customeradmin",
      },
      {
          "email": "continuoushack2@gmail.com",
          "firstLogin": "2018-02-28 11:54:12",
          "invitationState": "CONFIRMED",
          "lastLogin": "2020-03-23 10:45:37",
          "phoneNumber": "-",
          "responsibility": "Test",
          "role": "customeradmin",
      },
    ]


async def test_project_filtered():
    """Check for project mutation."""
    query = '''
      query {
        project(projectName: "unittesting"){
          findings(filters: {affectedSystems: "test", actor: "ANY_EMPLOYEE"}) {
            id
          }
        }
      }
    '''
    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert len(result['data']['project']['findings']) == 1
    assert result['data']['project']['findings'][0]['id'] == "463461507"


async def test_project_filter_not_match():
    """Check for project mutation."""
    query = '''
      query {
        project(projectName: "unittesting"){
          findings(filters: {affectedSystems: "notexists"}) {
            id
          }
        }
      }
    '''
    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert len(result['data']['project']['findings']) == 0


@pytest.mark.changes_db
async def test_create_project():
    """Check for createProject mutation."""
    query = '''
    mutation {
        createProject(
            organization: "okada",
            description: "This is a new project from pytest",
            projectName: "%(name)s",
            subscription: CONTINUOUS,
            hasDrills: true,
            hasForces: true
        ) {
        success
        }
    }'''
    query = query % {'name': await get_name('group')}
    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']


@pytest.mark.changes_db
async def test_add_tags():
    """Check for addTags mutation."""
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
        'projectName': 'unittesting',
        'tagsData': json.dumps(['testing'])
    }
    data = {'query': query, 'variables': variables}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addTags']
    assert result['data']['addTags']['success']


@pytest.mark.changes_db
async def test_remove_tag():
    """Check for removeTag mutation."""
    query = '''
        mutation RemoveTagMutation($tagToRemove: String!, $projectName: String!) {
            removeTag (
            tag: $tagToRemove,
            projectName: $projectName,
            ) {
            success
            }
        }
    '''
    variables = {
        'projectName': 'oneshottest',
        'tagToRemove': 'another-tag'
    }
    data = {'query': query, 'variables': variables}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert 'success' in result['data']['removeTag']
    assert result['data']['removeTag']['success']


@pytest.mark.changes_db
async def test_add_project_consult_parent_zero():
    """Check for addProjectConsult mutation."""
    query = '''
      mutation {
        addProjectConsult(
          content: "Test comment",
          parent: "0",
          projectName: "unittesting",
        ) {
          success
          commentId
        }
      }
      '''
    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']


@pytest.mark.changes_db
async def test_add_project_consult_parent_non_zero():
    """Check for addProjectConsult mutation."""
    query = '''
      mutation {
        addProjectConsult(
          content: "Test comment",
          parent: "1545946228675",
          projectName: "unittesting",
        ) {
          success
          commentId
        }
      }
      '''
    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']


@pytest.mark.changes_db
@pytest.mark.parametrize(
    ['group_name', 'subscription', 'has_drills',
        'has_forces', 'has_integrates', 'expected'],
    [
        ['UNITTESTING', 'CONTINUOUS', 'true', 'true', 'true', True],
        ['ONESHOTTEST', 'ONESHOT', 'false', 'false', 'true', True],
    ]
)
async def test_edit_group_good(
    group_name,
    subscription,
    has_drills,
    has_forces,
    has_integrates,
    expected,
):
    query = f"""
        mutation {{
            editGroup(
                comments: "",
                groupName: "{group_name}",
                subscription: {subscription},
                hasDrills: {has_drills},
                hasForces: {has_forces},
                hasIntegrates: {has_integrates},
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert 'success' in result['data']['editGroup']
    assert result['data']['editGroup']['success'] == expected


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        'comments',
        'group_name',
        'subscription',
        'has_drills',
        'has_forces',
        'has_integrates',
        'reason',
        'expected',
    ],
    [
        # Configuration error, Drills requires Integrates
        ['', 'ONESHOTTEST', 'CONTINUOUS', 'true', 'false', 'false', 'NONE',
         'Exception - Drills is only available when Integrates is too'],
        # Configuration error, Forces requires Integrates
        ['', 'ONESHOTTEST', 'CONTINUOUS', 'false', 'true', 'false', 'NONE',
         'Exception - Forces is only available when Integrates is too'],
        # Configuration error, Forces requires Drills
        ['', 'ONESHOTTEST', 'CONTINUOUS', 'false', 'true', 'true', 'NONE',
         'Exception - Forces is only available when Drills is too'],
        # Configuration error, Forces requires CONTINUOUS
        ['', 'ONESHOTTEST', 'ONESHOT', 'false', 'true', 'true', 'NONE',
         'Exception - Forces is only available in projects of type Continuous'],
        # Input validation error, weird chars
        ['\xFF', 'UNITTESTING', 'CONTINUOUS', 'true', 'true', 'true', 'NONE',
         'Exception - Invalid characters'],
        # Input validation error, too long string
        ['-' * 251, 'UNITTESTING', 'CONTINUOUS', 'true', 'true', 'true', 'NONE',
         'Exception - Invalid field length in form'],
        # Invalid reason
        ['-', 'UNITTESTING', 'CONTINUOUS', 'true', 'true', 'true', 'ASDF',
         'Expected type EditGroupReason, found ASDF.'],

    ]
)
async def test_edit_group_bad(
    comments,
    group_name,
    subscription,
    has_drills,
    has_forces,
    has_integrates,
    reason,
    expected,
):
    query = f"""
        mutation {{
            editGroup(
                comments: "{comments}"
                groupName: "{group_name}",
                hasDrills: {has_drills},
                hasForces: {has_forces},
                hasIntegrates: {has_integrates},
                reason: {reason},
                subscription: {subscription},
            ) {{
                success
            }}
        }}
      """
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert result['errors'][0]['message'] \
        == expected


async def test_get_roots() -> None:
    query = '''
        query {
          drillsBlackGroup: project(projectName: "oneshottest") {
            roots {
              __typename
              ...on IPRoot {
                address
                id
                port
              }
              ...on URLRoot {
                host
                id
                path
                port
                protocol
              }
            }
            subscription
          }
          drillsWhiteGroup: project(projectName: "unittesting") {
            roots {
              __typename
              ...on GitRoot {
                branch
                environment
                environmentUrls
                gitignore
                id
                includesHealthCheck
                url
              }
            }
            subscription
          }
        }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['drillsBlackGroup']['subscription'] == 'oneshot'
    assert result['data']['drillsBlackGroup']['roots'] == [
        {
            '__typename': 'URLRoot',
            'host': 'app.fluidattacks.com',
            'id': '8493c82f-2860-4902-86fa-75b0fef76034',
            'path': '/',
            'port': 443,
            'protocol': 'HTTPS'
        },
        {
            '__typename': 'IPRoot',
            'address': '127.0.0.1',
            'id': 'd312f0b9-da49-4d2b-a881-bed438875e99',
            'port': 8080
        }
    ]

    assert result['data']['drillsWhiteGroup']['subscription'] == 'continuous'
    assert result['data']['drillsWhiteGroup']['roots'] == [
        {
            '__typename': 'GitRoot',
            'branch': 'master',
            'environment': 'production',
            'environmentUrls': ['https://app.fluidattacks.com'],
            'gitignore': [
                'bower_components/*',
                'node_modules/*'
            ],
            'id': '4039d098-ffc5-4984-8ed3-eb17bca98e19',
            'includesHealthCheck': True,
            'url': 'https://gitlab.com/fluidattacks/product'
        },
        {
            '__typename': 'GitRoot',
            'branch': 'develop',
            'environment': 'QA',
            'environmentUrls': [],
            'gitignore': [],
            'id': '765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            'includesHealthCheck': False,
            'url': 'https://gitlab.com/fluidattacks/integrates'
        }
    ]


async def test_get_toe_lines() -> None:
    query = '''
      query {
        project(projectName: "unittesting"){
          name
          roots{
            ... on GitRoot {
              id
              toeLines {
                filename
                modifiedDate
                modifiedCommit
                loc
                testedDate
                testedLines
                comments
              }
            }
          }
        }
      }
    '''
    result = await _get_result_async(
      {'query': query},
      user='unittest2@fluidattacks.com'
    )
    assert 'errors' not in result
    assert result['data']['project']['roots'] == [
      {
        'id': '4039d098-ffc5-4984-8ed3-eb17bca98e19',
        'toeLines': [
          {
            'filename': 'product/test/test#.config',
            'modifiedDate': '2019-08-01T00:00:00-05:00',
            'modifiedCommit': '983466z',
            'loc': 8,
            'testedDate': '2021-02-28T00:00:00-05:00',
            'testedLines': 4,
            'comments': 'comment test'
          }
        ]
      },
      {
        'id': '765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
        'toeLines': [
          {
            'filename': 'integrates_1/test2/test.sh',
            'modifiedDate': '2020-11-19T00:00:00-05:00',
            'modifiedCommit': '273412t',
            'loc': 120,
            'testedDate': '2021-01-20T00:00:00-05:00',
            'testedLines': 172,
            'comments': 'comment test'
          }
        ]
      }
    ]


async def test_add_git_root_black() -> None:
    query = '''
      mutation {
        addGitRoot(
          branch: "master"
          environment: "Test"
          gitignore: []
          groupName: "oneshottest"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'


@pytest.mark.changes_db  # type: ignore
async def test_add_git_root_white() -> None:
    query = '''
      mutation {
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addGitRoot']['success']


async def test_add_git_root_invalid_branch() -> None:
    query = '''
      mutation {
        addGitRoot(
          branch: "( ͡° ͜ʖ ͡°)"
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


async def test_add_git_root_invalid_url() -> None:
    query = '''
      mutation {
        addGitRoot(
          branch: "master"
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "randomstring"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_add_git_root_uniqueness() -> None:
    query = '''
      mutation {
        addGitRoot(
          branch: "unique"
          environment: "unique"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/unique.git"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addGitRoot']['success']

    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'same Nickname already exists' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_add_ip_root_black() -> None:
    query = '''
      mutation {
        addIpRoot(address: "8.8.8.8", groupName: "oneshottest", port: 53) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addIpRoot']['success']


async def test_add_ip_root_white() -> None:
    query = '''
      mutation {
        addIpRoot(address: "8.8.8.8", groupName: "unittesting", port: 53) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'


async def test_add_ip_root_invalid_ip() -> None:
    query = '''
      mutation {
        addIpRoot(address: "randomstr", groupName: "oneshottest", port: 53) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


async def test_add_ip_root_invalid_port() -> None:
    query = '''
      mutation {
        addIpRoot(address: "8.8.8.8", groupName: "oneshottest", port: -2600) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_add_ip_root_uniqueness() -> None:
    query = '''
      mutation {
        addIpRoot(address: "1.1.1.1", groupName: "oneshottest", port: 53) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addIpRoot']['success']

    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'One or more values already exist' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_add_url_root_black() -> None:
    query = '''
      mutation {
        addUrlRoot(
          groupName: "oneshottest",
          url: "https://fluidattacks.com/"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addUrlRoot']['success']


async def test_add_url_root_white() -> None:
    query = '''
      mutation {
        addUrlRoot(
          groupName: "unittesting",
          url: "https://fluidattacks.com/"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'


async def test_add_url_root_invalid_url() -> None:
    query = '''
      mutation {
        addUrlRoot(groupName: "oneshottest", url: "randomstring") {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


async def test_add_url_root_invalid_protocol() -> None:
    query = '''
      mutation {
        addUrlRoot(groupName: "oneshottest", url: "ssh://test.com:22") {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'value is not valid' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_add_url_root_uniqueness() -> None:
    query = '''
      mutation {
        addUrlRoot(groupName: "oneshottest", url: "https://unique.com/") {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['addUrlRoot']['success']

    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'One or more values already exist' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_update_git_root() -> None:
    query = '''
      mutation {
        updateGitRoot(
          environment: "staging"
          gitignore: []
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          includesHealthCheck: false
          nickname: "randomNick"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['updateGitRoot']['success']


async def test_update_git_root_nonexistent() -> None:
    query = '''
      mutation {
        updateGitRoot(
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          id: "some-thing"
          includesHealthCheck: false
          nickname: "unique2"
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'root not found' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_update_git_environments() -> None:
    query = '''
      mutation {
        updateGitEnvironments(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          environmentUrls: ["https://app.fluidattacks.com/"]
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['updateGitEnvironments']['success']


@pytest.mark.changes_db  # type: ignore
async def test_update_root_cloning_status() -> None:
    query = '''
    mutation {
      updateRootCloningStatus(
        groupName: "unittesting"
        id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
        status: OK
        message: "root update test"
      ) {
        success
      }
    }
  '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['updateRootCloningStatus']['success']


@pytest.mark.changes_db  # type: ignore
async def test_update_root_cloning_status_nonexistent() -> None:
    query = '''
    mutation {
      updateRootCloningStatus(
        groupName: "unittesting"
        id: "4039d098-ffc5-4984-8ed3-eb17bca98e199"
        status: OK
        message: "root update test"
      ) {
        success
      }
    }
  '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'root not found' in result['errors'][0]['message']


@pytest.mark.changes_db  # type: ignore
async def test_update_root_state() -> None:
    query = '''
      mutation {
        updateRootState(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          state: INACTIVE
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' not in result
    assert result['data']['updateRootState']['success']


async def test_update_root_state_nonexistent() -> None:
    query = '''
      mutation {
        updateRootState(
          groupName: "unittesting"
          id: "some-thing"
          state: INACTIVE
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'root not found' in result['errors'][0]['message']


@pytest.mark.changes_db
async def test_unsubscribe_from_group() -> None:
    query = '''
      mutation {
        unsubscribeFromGroup(groupName: "metropolis"){
          success
        }
      }
    '''
    result = await _get_result_async(
      {'query': query},
      user='integratesuser@gmail.com'
    )

    assert 'errors' not in result
    assert result['data']['unsubscribeFromGroup']['success']
