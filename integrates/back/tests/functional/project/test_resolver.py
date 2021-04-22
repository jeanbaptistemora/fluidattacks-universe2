# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('project')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_get_project(populate: bool, email: str):
    assert populate
    group_name: str = 'group1'
    consult: str = 'This is a test comment'
    finding: str = '475041521'
    event: str = '418900971'
    root: str = '63298a73-9dff-46cf-b42d-9b2f01a56690'
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Exception - Document not found'
    assert result['data']['project']['name'] == group_name
    assert result['data']['project']['hasDrills']
    assert result['data']['project']['hasForces']
    assert result['data']['project']['hasIntegrates']
    assert result['data']['project']['openVulnerabilities'] == 1
    assert result['data']['project']['closedVulnerabilities'] == 1
    assert result['data']['project']['lastClosingVuln'] == 40
    assert result['data']['project']['maxSeverity'] == 4.1
    assert result['data']['project']['meanRemediate'] == 2
    assert result['data']['project']['meanRemediateCriticalSeverity'] == 0
    assert result['data']['project']['meanRemediateHighSeverity'] == 0
    assert result['data']['project']['meanRemediateLowSeverity'] == 3
    assert result['data']['project']['meanRemediateMediumSeverity'] == 4
    assert result['data']['project']['openFindings'] == 1
    assert result['data']['project']['totalFindings'] == 1
    assert result['data']['project']['totalTreatment'] == '{}'
    assert result['data']['project']['subscription'] == 'continuous'
    assert result['data']['project']['deletionDate'] == ''
    assert result['data']['project']['userDeletion'] == ''
    assert result['data']['project']['tags'] == ['testing']
    assert result['data']['project']['description'] == 'this is group1'
    assert result['data']['project']['serviceAttributes'] == [
        'has_drills_white',
        'has_forces',
        'has_integrates',
        'is_continuous',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers'
    ]
    assert result['data']['project']['organization'] == 'orgtest'
    assert result['data']['project']['userRole'] == email.split("@")[0]
    assert result['data']['project']['maxOpenSeverity'] == 4.3
    assert result['data']['project']['maxOpenSeverityFinding'] == None
    assert result['data']['project']['lastClosingVulnFinding'] == None
    assert result['data']['project']['maxSeverityFinding'] == {'analyst': 'admin@gmail.com'}
    assert consult in [consult['content'] for consult in result['data']['project']['consulting']]
    assert finding in [finding['id'] for finding in result['data']['project']['findings']]
    assert event in [event['id'] for event in result['data']['project']['events']]
    assert root in [root['id'] for root in result['data']['project']['roots']]
