import pytest

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphql.type import GraphQLResolveInfo
from jose import jwt
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.api.resolvers import tag

pytestmark = pytest.mark.asyncio


class TagTests(TestCase):

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
        request = RequestFactory().get('/')
        request.loaders = {
            'project': ProjectLoader(),
        }
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesuser@gmail.com'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'company': 'unittest'
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
        assert 'errors' not in result
        assert 'projects' in result['data']['tag']
        assert result['data']['tag']['lastClosingVuln'] == 23
        assert result['data']['tag']['meanRemediateLowSeverity'] == 116
        assert result['data']['tag']['meanRemediateMediumSeverity'] == 143.5
        assert result['data']['tag']['meanRemediate'] == 174
        assert result['data']['tag']['maxOpenSeverity'] == 4.9
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
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesuser@gmail.com'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'company': 'unittest'
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
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'Access denied'
