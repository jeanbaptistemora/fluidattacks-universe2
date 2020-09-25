import pytest

from datetime import datetime, timedelta

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.project import ProjectLoader
from backend.api.schema import SCHEMA
from backend.dal.user import get_projects
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class MeTests(TestCase):

    async def test_me(self):
        """Check Me query"""
        query = '''{
            me(callerOrigin: "API") {
                accessToken
                projects {
                    name
                    description
                }
                tags(organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3") {
                    name
                    projects {
                        name
                    }
                }
                remember
                role(entity: USER)
                permissions(entity: USER)
                callerOrigin
                __typename
            }
        }'''
        data = {'query': query}
        user_email = 'integratesuser@gmail.com'
        request = await create_dummy_session(user_email)
        request.loaders = {
            'project': ProjectLoader(),
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        expected_groups = ['unittesting', 'oneshottest']
        assert 'me' in result['data']
        assert 'role' in result['data']['me']
        assert result['data']['me']['role'] == 'customeradmin'
        assert result['data']['me']['permissions'] == []
        assert result['data']['me']['callerOrigin'] == 'API'
        assert 'projects' in result['data']['me']
        assert 'tags' in result['data']['me']
        for tag in result['data']['me']['tags']:
            assert 'name' in tag
            assert 'projects' in tag
            if tag['name'] == 'test-projects':
                output = [proj['name'] for proj in tag['projects']]
                assert sorted(output) == sorted(expected_groups)
        for project in result['data']['me']['projects']:
            assert 'name' in project
            assert 'description' in project
        groups = [prj['name'] for prj in result['data']['me']['projects']]
        assert sorted(expected_groups) == sorted(groups)
        all_user_groups = await get_projects(user_email, True)
        assert len(groups) < len(all_user_groups)
        self.assertFalse(groups == all_user_groups)

    @pytest.mark.changes_db
    async def test_sign_in(self):
        """Check for signIn mutation."""
        query = '''
            mutation {
                signIn(
                    authToken: "badtoken",
                    provider: GOOGLE
                ) {
                    sessionJwt
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert not result['data']['signIn']['success']

    @pytest.mark.changes_db
    async def test_update_access_token(self):
        """Check for updateAccessToken mutation."""
        query = '''
            mutation updateAccessToken ($expirationTime: Int!) {
                updateAccessToken(expirationTime: $expirationTime) {
                    sessionJwt
                    success
                }
            }
        '''
        expiration_time = datetime.utcnow() + timedelta(weeks=8)
        expiration_time = int(expiration_time.timestamp())

        data = {
            'query': query,
            'variables': {
                'expirationTime': expiration_time
            }
        }
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'updateAccessToken' in result['data']
        assert 'success' in result['data']['updateAccessToken']

    @pytest.mark.changes_db
    async def test_invalidate_access_token(self):
        """Check invalidateAccessToken query"""
        query = '''
            mutation {
                invalidateAccessToken {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'invalidateAccessToken' in result['data']
        assert 'success' in result['data']['invalidateAccessToken']

    @pytest.mark.changes_db
    async def test_accept_legal(self):
        """Check acceptLegal query"""
        query = '''
            mutation {
                acceptLegal(remember: true) {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'acceptLegal' in result['data']
        assert 'success' in result['data']['acceptLegal']

    @pytest.mark.changes_db
    async def test_add_push_token(self):
        """Check add_push_token mutation"""
        query = '''
            mutation {
                addPushToken(token: "ExponentPushToken[something123]") {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'error' not in result
        assert result['data']['addPushToken']['success']
