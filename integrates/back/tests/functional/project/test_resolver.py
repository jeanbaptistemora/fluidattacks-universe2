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
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group1'
    consult: str = 'This is a test comment'
    finding: str = '475041521'
    event: str = '418900971'
    root: str = '63298a73-9dff-46cf-b42d-9b2f01a56690'
    draft = {
        'id': '475041531',
        'title': 'FIN.H.060. Insecure exceptions',
    }
    stakeholders: str = [
        'analyst@gmail.com',
        'closer@gmail.com',
        'customer@gmail.com',
        'customeradmin@gmail.com',
        'executive@gmail.com',
        'resourcer@gmail.com',
        'reviewer@gmail.com',
    ]
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group=group_name
    )
    print(sorted([stakeholder['email'] for stakeholder in result['data']['project']['stakeholders']]))
    assert 'errors' in result
    assert len(result['errors']) == 1
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
    assert result['data']['project']['userRole'] == 'admin'
    assert result['data']['project']['maxOpenSeverity'] == 4.3
    assert result['data']['project']['maxOpenSeverityFinding'] == None
    assert result['data']['project']['lastClosingVulnFinding'] == None
    assert result['data']['project']['maxSeverityFinding'] == {'analyst': 'admin@gmail.com'}
    assert consult in [consult['content'] for consult in result['data']['project']['consulting']]
    assert finding in [finding['id'] for finding in result['data']['project']['findings']]
    assert event in [event['id'] for event in result['data']['project']['events']]
    assert root in [root['id'] for root in result['data']['project']['roots']]
    assert draft in result['data']['project']['drafts']
    assert stakeholders == sorted([stakeholder['email'] for stakeholder in result['data']['project']['stakeholders']])



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('project')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group1'
    consult: str = 'This is a test comment'
    finding: str = '475041521'
    event: str = '418900971'
    root: str = '63298a73-9dff-46cf-b42d-9b2f01a56690'
    draft = {
        'id': '475041531',
        'title': 'FIN.H.060. Insecure exceptions',
    }
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group=group_name
    )
    assert 'errors' in result
    assert len(result['errors']) == 2
    assert result['errors'][0]['message'] == 'Exception - Document not found'
    assert result['errors'][1]['message'] == 'Access denied'
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
    assert result['data']['project']['userRole'] == 'analyst'
    assert result['data']['project']['maxOpenSeverity'] == 4.3
    assert result['data']['project']['maxOpenSeverityFinding'] == None
    assert result['data']['project']['lastClosingVulnFinding'] == None
    assert result['data']['project']['maxSeverityFinding'] == {'analyst': 'admin@gmail.com'}
    assert consult in [consult['content'] for consult in result['data']['project']['consulting']]
    assert finding in [finding['id'] for finding in result['data']['project']['findings']]
    assert event in [event['id'] for event in result['data']['project']['events']]
    assert root in [root['id'] for root in result['data']['project']['roots']]
    assert draft in result['data']['project']['drafts']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('project')
async def test_closer(populate: bool):
    assert populate
    group_name: str = 'group1'
    consult: str = 'This is a test comment'
    finding: str = '475041521'
    event: str = '418900971'
    root: str = '63298a73-9dff-46cf-b42d-9b2f01a56690'
    draft = {
        'id': '475041531',
        'title': 'FIN.H.060. Insecure exceptions',
    }
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        group=group_name
    )
    assert 'errors' in result
    assert len(result['errors']) == 3
    assert result['errors'][0]['message'] == 'Exception - Document not found'
    assert result['errors'][1]['message'] == 'Access denied'
    assert result['errors'][2]['message'] == 'Access denied'
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
    assert result['data']['project']['userRole'] == 'closer'
    assert result['data']['project']['maxOpenSeverity'] == 4.3
    assert result['data']['project']['maxOpenSeverityFinding'] == None
    assert result['data']['project']['lastClosingVulnFinding'] == None
    assert result['data']['project']['maxSeverityFinding'] == {'analyst': 'admin@gmail.com'}
    assert consult in [consult['content'] for consult in result['data']['project']['consulting']]
    assert finding in [finding['id'] for finding in result['data']['project']['findings']]
    assert event in [event['id'] for event in result['data']['project']['events']]
    assert root in [root['id'] for root in result['data']['project']['roots']]
