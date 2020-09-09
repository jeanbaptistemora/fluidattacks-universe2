import json
import os
from datetime import datetime, timedelta
import random
import string
import pytest

from ariadne import graphql, graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.domain.available_name import get_name
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied

from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


def random_project_name(string_length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class ProjectTests(TestCase):

    async def _get_result_async(self, data, user='integratesmanager@gmail.com'):
        """Get result."""
        request = await create_dummy_session(username=user)
        request.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'project': ProjectLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    async def test_project(self):
        """Check for project mutation."""
        query = '''
          query {
            project(projectName: "unittesting"){
              name
              remediatedOverTime
              hasDrills
              hasForces
              findings {
                  analyst
              }
              hasIntegrates
              openVulnerabilities
              closedVulnerabilities
              lastClosingVuln
              pendingClosingCheck
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
              users {
                  email
                  role
              }
              __typename
            }
          }
        '''
        data = {'query': query}
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert result['data']['project']['name'] == 'unittesting'
        assert 'remediatedOverTime' in result['data']['project']
        assert result['data']['project']['hasDrills']
        assert result['data']['project']['hasForces']
        assert len(result['data']['project']['findings']) == 6
        assert result['data']['project']['openVulnerabilities'] == 31
        assert result['data']['project']['closedVulnerabilities'] == 8
        assert 'lastClosingVuln' in result['data']['project']
        assert result['data']['project']['pendingClosingCheck'] == 2
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
        assert len(result['data']['project']['users']) == 5

    async def test_project_filtered(self):
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert len(result['data']['project']['findings']) == 1
        assert result['data']['project']['findings'][0]['id'] == "463461507"

    async def test_project_filter_not_match(self):
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert len(result['data']['project']['findings']) == 0

    async def test_alive_projects(self):
        """Check for projects mutation."""
        query = '''
          query {
            projects
          }
        '''
        data = {'query': query}
        expected_projects = [
            'suspendedtest',
            'oneshottest',
            'unittesting',
            'continuoustesting'
        ]

        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert result['data']['projects'] == expected_projects

    @pytest.mark.changes_db
    async def test_create_project(self):
        """Check for createProject mutation."""
        query = '''
        mutation {
            createProject(
                organization: "imamura",
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
        result = await self._get_result_async(data, user='integratesuser@gmail.com')
        assert 'errors' not in result
        assert 'success' in result['data']['createProject']
        assert result['data']['createProject']['success']

    @pytest.mark.changes_db
    async def test_reject_request_remove_denied(self):
        """Check for rejectRemoveProject mutation."""
        query = '''
        mutation RejectRemoveProjectMutation(
                $projectName: String!,
            ){
            rejectRemoveProject(projectName: $projectName) {
            success
           }
        }'''
        variables = {
            'projectName': 'PendingprojecT'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result_async(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())

    @pytest.mark.changes_db
    async def test_reject_request_remove_not_pending(self):
        """Check for rejectRemoveProject mutation."""
        query = '''
        mutation RejectRemoveProjectMutation(
                $projectName: String!,
            ){
            rejectRemoveProject(projectName: $projectName) {
            success
           }
        }'''
        variables = {
            'projectName': 'unittesting'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result_async(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(NotPendingDeletion())

    @pytest.mark.changes_db
    async def test_add_tags(self):
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addTags']
        assert result['data']['addTags']['success']

    @pytest.mark.changes_db
    async def test_remove_tag(self):
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeTag']
        assert result['data']['removeTag']['success']

    @pytest.mark.changes_db
    async def test_add_project_comment_parent_zero(self):
        """Check for addProjectComment mutation."""
        query = '''
          mutation {
            addProjectComment(
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addProjectComment']
        assert result['data']['addProjectComment']['success']

    @pytest.mark.changes_db
    async def test_add_project_comment_parent_non_zero(self):
        """Check for addProjectComment mutation."""
        query = '''
          mutation {
            addProjectComment(
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
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addProjectComment']
        assert result['data']['addProjectComment']['success']


@pytest.mark.changes_db
@pytest.mark.parametrize(
    ['group_name', 'subscription', 'has_drills', 'has_forces', 'has_integrates', 'expected'],
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
    result = await ProjectTests._get_result_async(None, {
        'query': query,
    })

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
    result = await ProjectTests._get_result_async(None, {
        'query': query,
    })

    assert 'errors' in result
    assert result['errors'][0]['message'] \
        == expected
