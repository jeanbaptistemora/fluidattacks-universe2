import pytest

from django.test import TestCase
from graphql.error import GraphQLError
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt
from .test_utils import Request

from backend.entity.user import (validate_email_address,
                                 validate_field,
                                 validate_phone_field)
from backend.api.schema import SCHEMA


class UserTests(TestCase):

    def test_grant_user_access(self):
        testing_client = Client(SCHEMA)
        query = '''
            mutation {
                grantUserAccess (
                email: "test@test.test",
                organization: "test",
                phoneNumber: "3453453453"
                projectName: "unittesting",
                responsibility: "test",
                role: "customer") {
                success
                grantedUser {
                    email
                    role
                    responsibility
                    phoneNumber
                    organization
                    firstLogin
                    lastLogin
                }
                }
            }
        '''
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantUserAccess']

    def test_get_user(self):
        testing_client = Client(SCHEMA)
        query = '''
            query {
                user(projectName: "unittesting",
                     userEmail: "continuoushacking@gmail.com") {
                    organization
                    responsibility
                    phoneNumber
                }
            }
        '''
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'user' in result['data']

    def test_add_user(self):
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        query = '''
            mutation {
              grantUserAccess (
                email: "test@test.test",
                organization: "test",
                phoneNumber: "7357",
                projectName: "unittesting",
                responsibility: "test",
                  role: "customer") {
                    success
                      grantedUser {
                        email
                        role
                        responsibility
                        phoneNumber
                        organization
                        firstLogin
                        lastLogin
                    }
                }
            }
        '''
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantUserAccess']

    def test_remove_user(self):
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        query = '''
            mutation {
              removeUserAccess (
                projectName: "unittesting"
                userEmail: "test@test.test"
                )
                {
                  removedEmail
                  success
                }
            }
        '''
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'success' in result['data']['removeUserAccess']

    def test_edit_user(self):
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        query = '''
            mutation {
              editUser (
                email: "test@test.testedited",
                organization: "edited",
                phoneNumber: "17364735",
                projectName: "unittesting",
                responsibility: "edited",
                role: "customer") {
                  success
                }
            }
        '''
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'success' in result['data']['editUser']

    def test_validate_email_address(self):
        """makes sure that the email is being validated properly"""
        assert validate_email_address('test@test.test')
        assert validate_email_address('test.test@test.test')
        assert validate_email_address('test.test@test.test.test')
        with pytest.raises(GraphQLError):
            assert validate_email_address('test@test')
        with pytest.raises(GraphQLError):
            assert validate_email_address('test')

    def test_validate_field(self):
        """makes sure that the  field is filtering only = sign at start"""
        assert validate_field('t35t 7 test @ test')
        with pytest.raises(GraphQLError):
            assert validate_field('=test')

    def test_validate_phone_number(self):
        assert validate_phone_field("123123123")
        with pytest.raises(GraphQLError):
            assert validate_phone_field("asdasdasd")
        with pytest.raises(GraphQLError):
            assert validate_phone_field("=12123123123")
