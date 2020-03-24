import json
import os

from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied


class ProjectTests(TestCase):

    def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'user_role': 'admin',
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        return result

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
