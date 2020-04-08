import pytest

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphql.type import GraphQLResolveInfo
from jose import jwt
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
                    name
                    projects {
                        closedVulnerabilities
                        name
                        openVulnerabilities
                    }
                }
            }
        '''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'projects' in result['data']['tag']
