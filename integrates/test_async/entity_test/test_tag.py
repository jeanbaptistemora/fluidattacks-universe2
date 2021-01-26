import pytest

from ariadne import graphql
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_tag_query():
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
        'finding_vulns': FindingVulnsLoader(),
        'group': GroupLoader()
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'projects' in result['data']['tag']
    assert result['data']['tag']['lastClosingVuln'] == 50
    assert result['data']['tag']['meanRemediateLowSeverity'] == 116
    assert result['data']['tag']['meanRemediateMediumSeverity'] == 135.9
    assert result['data']['tag']['meanRemediate'] == 123
    assert result['data']['tag']['maxOpenSeverity'] == 3.3
    assert result['data']['tag']['maxSeverity'] == 4.3

async def test_get_tag_query_access_denied():
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
        'finding_vulns': FindingVulnsLoader(),
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied or tag not found'
