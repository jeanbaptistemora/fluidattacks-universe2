import json
import os
import random
import string
import pytest

from ariadne import graphql, graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied

pytestmark = pytest.mark.asyncio


def random_project_name(string_length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class ProjectTests(TestCase):

    async def _get_result_async(self, data, user=None):
        """Get result."""
        user = user or 'integratesmanager@gmail.com'
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': user,
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
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
              comments {
                content
              }
              drafts {
                age
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
        assert len(result['data']['project']['events']) == 5
        assert result['data']['project']['comments'][0]['content'] == 'Now we can post comments on projects'
        assert len(result['data']['project']['users']) == 4

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
            projects {
              name
            }
          }
        '''
        data = {'query': query}
        expected_projects = [
            {'name': 'suspendedtest'},
            {'name': 'oneshottest'},
            {'name': 'unittesting'},
            {'name': 'continuoustesting'}
        ]

        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert result['data']['projects'] == expected_projects

    async def test_alive_projects_filtered(self):
        """Check for projects mutation."""
        query = '''
          query {
            projects(filters: {name: "unittesting"}) {
              subscription
            }
          }
        '''
        data = {'query': query}
        expected_output = [
            {'subscription': 'continuous'}
        ]

        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert result['data']['projects'] == expected_output

    @pytest.mark.changes_db
    async def test_create_project(self):
        """Check for createProject mutation."""
        query = '''
        mutation {
            createProject(
                companies: ["fluid"],
                description: "This is a new project from pytest",
                projectName: "%(project_name)s",
                subscription: CONTINUOUS,
                hasDrills: true,
                hasForces: true
            ) {
            success
           }
        }'''
        query = query % {'project_name': random_project_name()}
        data = {'query': query}
        result = await self._get_result_async(data, user='unittest@fluidattacks.com')
        if 'errors' not in result:
            assert 'errors' not in result
            assert 'success' in result['data']['createProject']
            assert result['data']['createProject']['success']
        else:
            pytest.skip("Expected error")

    @pytest.mark.changes_db
    async def test_request_remove_denied(self):
        """Check for createProject mutation."""
        query = '''
        mutation RequestRemoveProjectMutation(
                $projectName: String!,
            ){
            requestRemoveProject(projectName: $projectName) {
            success
           }
        }'''
        variables = {
            'projectName': 'OneshottesT'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result_async(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())

    @pytest.mark.changes_db
    async def test_request_remove_pending(self):
        """Check for requestRemoveProject mutation."""
        query = '''
        mutation RequestRemoveProjectMutation(
                $projectName: String!,
            ){
            requestRemoveProject(projectName: $projectName) {
            success
           }
        }'''
        variables = {
            'projectName': 'pendingproject'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result_async(data)
        assert 'errors' in result
        # You need Integrates in order to request deletion
        assert result['errors'][0]['message'] == 'Access denied'

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
    async def test_add_all_project_access(self):
        """Check for addAllProjectAccess mutation."""
        query = '''
            mutation {
                addAllProjectAccess(projectName: "UNITTESTING")
                    {
                        success
                    }
            }

        '''
        data = {'query': query}
        result = await self._get_result_async(data, user='unittest@fluidattacks.com')
        assert 'errors' not in result
        assert 'success' in result['data']['addAllProjectAccess']
        assert result['data']['addAllProjectAccess']['success']

    @pytest.mark.changes_db
    async def test_remove_all_project_access(self):
        """Check for removeAllProjectAccess mutation."""
        query = '''
            mutation {
                removeAllProjectAccess(projectName: "ONESHOTTEST")
                    {
                        success
                    }
            }

        '''
        data = {'query': query}
        result = await self._get_result_async(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeAllProjectAccess']
        assert result['data']['removeAllProjectAccess']['success']

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
                groupName: "{group_name}",
                subscription: {subscription},
                hasDrills: {has_drills},
                hasForces: {has_forces},
                hasIntegrates: {has_integrates},
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


@pytest.mark.parametrize(
    ['group_name', 'subscription', 'has_drills', 'has_forces', 'has_integrates', 'expected'],
    [
        # Configuration error, Drills requires Integrates
        ['ONESHOTTEST', 'CONTINUOUS', 'true', 'false', 'false',
         'Exception - Drills is only available when Integrates is too'],
        # Configuration error, Forces requires Integrates
        ['ONESHOTTEST', 'CONTINUOUS', 'false', 'true', 'false',
         'Exception - Forces is only available when Integrates is too'],
        # Configuration error, Forces requires Drills
        ['ONESHOTTEST', 'CONTINUOUS', 'false', 'true', 'true',
         'Exception - Forces is only available when Drills is too'],
        # Configuration error, Forces requires CONTINUOUS
        ['ONESHOTTEST', 'ONESHOT', 'false', 'true', 'true',
         'Exception - Forces is only available in projects of type Continuous'],
    ]
)
async def test_edit_group_bad(
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
                groupName: "{group_name}",
                subscription: {subscription},
                hasDrills: {has_drills},
                hasForces: {has_forces},
                hasIntegrates: {has_integrates},
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
