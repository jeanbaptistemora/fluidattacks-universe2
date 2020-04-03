import json
import os

from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied


class ProjectTests(TestCase):

    def _get_result(self, data, user=None):
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
            'vulnerability': VulnerabilityLoader()
        }
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        return result

    def test_project(self):
        """Check for project mutation."""
        query = '''
          query {
            project(projectName: "unittesting"){
              name,
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
              totalFindings
              totalTreatment
              currentMonthAuthors
              currentMonthCommits
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
            }
          }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' not in result
        assert result['data']['project']['name'] == 'unittesting'
        assert 'remediatedOverTime' in result['data']['project']
        assert result['data']['project']['hasDrills']
        assert result['data']['project']['hasForces']
        assert len(result['data']['project']['findings']) == 5
        assert result['data']['project']['openVulnerabilities'] == 14
        assert result['data']['project']['closedVulnerabilities'] == 7
        assert 'lastClosingVuln' in result['data']['project']
        assert result['data']['project']['pendingClosingCheck'] == 2
        assert result['data']['project']['maxSeverity'] == 4.3
        assert result['data']['project']['meanRemediate'] == 245
        assert result['data']['project']['totalFindings'] == 5
        assert 'totalTreatment' in result['data']['project']
        assert result['data']['project']['currentMonthAuthors'] == 0
        assert result['data']['project']['currentMonthCommits'] == 0
        assert result['data']['project']['subscription'] == 'continuous'
        assert result['data']['project']['deletionDate'] == ''
        assert result['data']['project']['userDeletion'] == ''
        assert result['data']['project']['tags'][0] == 'testing'
        assert result['data']['project']['description'] == 'Integrates unit test project'
        assert len(result['data']['project']['drafts']) == 2
        assert len(result['data']['project']['events']) == 5
        assert result['data']['project']['comments'][0]['content'] == 'Now we can post comments on projects'
        assert len(result['data']['project']['users']) == 4

    def test_create_project(self):
        """Check for createProject mutation."""
        query = '''
        mutation {
            createProject(
                companies: ["fluid"],
                description: "This is a new project from pytest",
                projectName: "ANEWPROJECT",
                subscription: CONTINUOUS,
                hasDrills: true,
                hasForces: true
            ) {
            success
           }
        }'''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['createProject']
        assert result['data']['createProject']['success']

    def test_request_remove_denied(self):
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
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())

    def test_request_remove_pending(self):
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
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(AlreadyPendingDeletion())

    def test_reject_request_remove_denied(self):
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
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())

    def test_reject_request_remove_not_pending(self):
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
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(NotPendingDeletion())

    def test_add_tags(self):
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addTags']
        assert result['data']['addTags']['success']

    def test_remove_tag(self):
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
            'projectName': 'unittesting',
            'tagToRemove': 'test-projects'
        }
        data = {'query': query, 'variables': variables}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeTag']
        assert result['data']['removeTag']['success']

    def test_add_all_project_access(self):
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
        result = self._get_result(data, user='unittest@fluidattacks.com')
        assert 'errors' not in result
        assert 'success' in result['data']['addAllProjectAccess']
        assert result['data']['addAllProjectAccess']['success']

    def test_remove_all_project_access(self):
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeAllProjectAccess']
        assert result['data']['removeAllProjectAccess']['success']
