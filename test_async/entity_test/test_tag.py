from datetime import datetime, timedelta
import pytest

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphql.type import GraphQLResolveInfo
from jose import jwt
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.api.resolvers import tag

pytestmark = pytest.mark.asyncio


class TagTests(TestCase):

    def create_dummy_session(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesuser@gmail.com'
        request.session['company'] = 'unittest'
        payload = {
            'user_email': 'integratesuser@gmail.com',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': util.calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        request.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'project': ProjectLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        return request

    @pytest.mark.asyncio
    async def test_get_tag_query(self):
        """Check for project alert."""
        query = '''
            query{
                tag(tag: "test-projects"){
                    lastClosingVuln
                    maxOpenSeverity
                    maxSeverity
                    meanRemediateLowSeverity
                    meanRemediateMediumSeverity
                    meanRemediate
                    name
                    projects {
                        closedVulnerabilities
                        name
                        openVulnerabilities
                    }
                    __typename
                }
            }
        '''
        data = {'query': query}
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'projects' in result['data']['tag']
        assert result['data']['tag']['lastClosingVuln'] == 23
        assert result['data']['tag']['meanRemediateLowSeverity'] == 116
        assert result['data']['tag']['meanRemediateMediumSeverity'] == 143.5
        assert result['data']['tag']['meanRemediate'] == 174
        assert result['data']['tag']['maxOpenSeverity'] == 6.3
        assert result['data']['tag']['maxSeverity'] == 6.3

    async def test_get_tag_query_access_denied(self):
        query = '''
            query{
                tag(tag: "another-tag"){
                    lastClosingVuln
                    maxOpenSeverity
                    meanRemediate
                    name
                    projects {
                        closedVulnerabilities
                        name
                        openVulnerabilities
                    }
                    __typename
                }
            }
        '''
        data = {'query': query}
        
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'Access denied'
