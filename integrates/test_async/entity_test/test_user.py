from datetime import datetime, timedelta
import pytest

from ariadne import graphql, graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class UserTests(TestCase):

    @pytest.mark.asyncio
    async def test_get_user(self):
        """Check for user."""
        query = '''
            query {
                stakeholder(entity: PROJECT,
                     projectName: "unittesting",
                     userEmail: "continuoushacking@gmail.com") {
                    email
                    role
                    responsibility
                    phoneNumber
                    firstLogin
                    lastLogin
                    projects {
                        name
                    }
                    __typename
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'stakeholder' in result['data']
        assert 'responsibility' in result['data']['stakeholder']
        assert 'phoneNumber' in result['data']['stakeholder']

    async def test_user_list_projects(self):
        """Check for user."""
        query = '''
            query {
                userListProjects(userEmail: "continuoushacking@gmail.com") {
                    name
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert result['data']['userListProjects'][0]['name'] == 'oneshottest'

    @pytest.mark.changes_db
    async def test_add_user(self):
        """Check for addStakeholder mutation."""
        query = '''
            mutation {
                addStakeholder(
                    email: "test@test.com",
                    role: CUSTOMER,
                    phoneNumber: "3331112233"
                ) {
                    success
                    email
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session('integratesmanager@gmail.com')
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'addStakeholder' in result['data']
        assert 'success' in result['data']['addStakeholder']
        assert 'email' in result['data']['addStakeholder']

    @pytest.mark.changes_db
    async def test_grant_user_access_1(self):
        """Check for grantStakeholderAccess mutation."""
        query = '''
            mutation {
                grantStakeholderAccess (
                email: "test@test.test",
                phoneNumber: "3453453453"
                projectName: "unittesting",
                responsibility: "test",
                role: CUSTOMER) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    phoneNumber
                    firstLogin
                    lastLogin
                }
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantStakeholderAccess']
        assert 'grantedStakeholder' in result['data']['grantStakeholderAccess']
        assert 'email' in result['data']['grantStakeholderAccess']['grantedStakeholder']

    @pytest.mark.changes_db
    async def test_grant_stakeholder_access_2(self):
        """Check for grantStakeholderAccess mutation."""
        query = '''
            mutation {
                grantStakeholderAccess (
                email: "test@test.test",
                phoneNumber: "3453453453"
                projectName: "unittesting",
                responsibility: "test",
                role: ANALYST) {
                    success
                    grantedStakeholder {
                        email
                        role
                        responsibility
                        phoneNumber
                        firstLogin
                        lastLogin
                    }
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' in result
        assert result['errors'][0]['message'] == (
            'Exception - Groups with any active Fluid Attacks service can '
            'only have Hackers provided by Fluid Attacks'
        )

    @pytest.mark.changes_db
    async def test_grant_stakeholder_access_3(self):
        """Check for grantStakeholderAccess mutation."""
        query = '''
            mutation {
                grantStakeholderAccess (
                email: "test@fluidattacks.com",
                phoneNumber: "3453453453"
                projectName: "unittesting",
                responsibility: "test",
                role: ANALYST) {
                    success
                    grantedStakeholder {
                        email
                        role
                        responsibility
                        phoneNumber
                        firstLogin
                        lastLogin
                    }
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantStakeholderAccess']
        assert 'grantedStakeholder' in result['data']['grantStakeholderAccess']
        assert 'email' in result['data']['grantStakeholderAccess']['grantedStakeholder']

    @pytest.mark.changes_db
    async def test_remove_stakeholder_access(self):
        """Check for removeStakeholderAccess mutation."""
        query = '''
            mutation {
              removeStakeholderAccess (
                projectName: "unittesting"
                userEmail: "test@test.test"
                )
                {
                  removedEmail
                  success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['removeStakeholderAccess']
        assert 'removedEmail' in result['data']['removeStakeholderAccess']

    @pytest.mark.changes_db
    async def test_edit_stakeholder(self):
        """Check for editStakeholder mutation."""
        query = '''
            mutation {
              editStakeholder (
                email: "test@test.testedited",
                phoneNumber: "17364735",
                projectName: "unittesting",
                responsibility: "edited",
                role: CUSTOMER) {
                  success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['editStakeholder']
