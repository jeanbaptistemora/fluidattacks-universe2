import json
import pytest

from ariadne import graphql
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.api.schema import SCHEMA
from backend.domain.available_name import get_name
from backend.exceptions import NotPendingDeletion, PermissionDenied

from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


async def _get_result_async(data, user='integratesmanager@gmail.com'):
    """Get result."""
    request = await create_dummy_session(username=user)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'finding_vulns': FindingVulnsLoader(),
        'group': GroupLoader(),
        'group_drafts': GroupDraftsLoader(),
        'group_findings': GroupFindingsLoader(),
        'group_roots': GroupRootsLoader(),
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result


async def test_project():
    """Check for project mutation."""
    query = '''
      query {
        project(projectName: "unittesting"){
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
          __typename
        }
      }
    '''
    data = {'query': query}
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
            'host': 'integrates.fluidattacks.com',
            'id': 'ROOT#8493c82f-2860-4902-86fa-75b0fef76034',
            'path': '/',
            'port': 443,
            'protocol': 'HTTPS'
        },
        {
            '__typename': 'IPRoot',
            'address': '127.0.0.1',
            'id': 'ROOT#d312f0b9-da49-4d2b-a881-bed438875e99',
            'port': 8080
        }
    ]

    assert result['data']['drillsWhiteGroup']['subscription'] == 'continuous'
    assert result['data']['drillsWhiteGroup']['roots'] == [
        {
            '__typename': 'GitRoot',
            'branch': 'master',
            'environment': 'production',
            'environmentUrls': ['https://integrates.fluidattacks.com'],
            'gitignore': [
                'bower_components/*',
                'node_modules/*'
            ],
            'id': 'ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19',
            'includesHealthCheck': True,
            'url': 'https://gitlab.com/fluidattacks/product'
        },
        {
            '__typename': 'GitRoot',
            'branch': 'develop',
            'environment': 'QA',
            'environmentUrls': [],
            'gitignore': [],
            'id': 'ROOT#765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            'includesHealthCheck': False,
            'url': 'https://gitlab.com/fluidattacks/integrates'
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
    assert 'same URL/branch already exists' in result['errors'][0]['message']


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
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19"
          includesHealthCheck: false
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
          id: "ROOT#some-thing"
          includesHealthCheck: false
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
          id: "ROOT#765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          environmentUrls: ["https://integrates.fluidattacks.com/"]
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
        id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19"
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
        id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e199"
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
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19"
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
          id: "ROOT#some-thing"
          state: INACTIVE
        ) {
          success
        }
      }
    '''
    result = await _get_result_async({'query': query})

    assert 'errors' in result
    assert 'root not found' in result['errors'][0]['message']
