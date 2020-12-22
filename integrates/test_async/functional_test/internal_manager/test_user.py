import pytest

from test_async.functional_test.internal_manager.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_user():
    query = f'''
        query {{
            userListProjects(userEmail: "continuoushacking@gmail.com") {{
                closedVulnerabilities
                deletionDate
                description
                hasDrills
                hasForces
                hasIntegrates
                lastClosingVuln
                maxOpenSeverity
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                name
                openFindings
                openVulnerabilities
                organization
                subscription
                tags
                userDeletion
                userRole
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['userListProjects'] ==  [
        {
            'closedVulnerabilities': 0,
            'deletionDate': '',
            'description': 'oneshot testing',
            'hasDrills': False,
            'hasForces': False,
            'hasIntegrates': True,
            'lastClosingVuln': 45,
            'maxOpenSeverity': 0.0,
            'meanRemediate': 103,
            'meanRemediateCriticalSeverity': 0,
            'meanRemediateHighSeverity': 0,
            'meanRemediateLowSeverity': 0,
            'meanRemediateMediumSeverity': 0,
            'name': 'oneshottest',
            'openFindings': 0,
            'openVulnerabilities': 0,
            'organization': 'okada',
            'subscription': 'oneshot',
            'tags': ['another-tag', 'test-projects'],
            'userDeletion': '',
            'userRole': ''
        },
        {
            'closedVulnerabilities': 8,
            'deletionDate': '',
            'description': 'Integrates unit test project',
            'hasDrills': True,
            'hasForces': True,
            'hasIntegrates': True,
            'lastClosingVuln': 23,
            'maxOpenSeverity': 6.3,
            'meanRemediate': 245,
            'meanRemediateCriticalSeverity': 0,
            'meanRemediateHighSeverity': 0,
            'meanRemediateLowSeverity': 232,
            'meanRemediateMediumSeverity': 287,
            'name': 'unittesting',
            'openFindings': 5,
            'openVulnerabilities': 31,
            'organization': 'okada',
            'subscription': 'continuous',
            'tags': ['test-projects'],
            'userDeletion': '',
            'userRole': 'internal_manager'
        }
    ]
