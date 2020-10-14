import pytest

from ariadne import graphql
from django.test import TestCase
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session

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
        request = await create_dummy_session('integratesuser@gmail.com')
        request.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'group': GroupLoader(),
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

        request = await create_dummy_session('unittests')
        request.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'project': ProjectLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'Access denied or tag not found'
