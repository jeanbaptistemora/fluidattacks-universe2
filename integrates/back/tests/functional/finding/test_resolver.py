# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('finding')
async def test_admin(populate: bool):
    assert populate
    open_vuln: str = '6401bc87-8633-4a4a-8d8e-7dae0ca57e6a'
    closed_vuln: str = 'be09edb7-cd5c-47ed-bee4-97c645acdce8'
    finding_id: str = '475041513'
    title: str = 'F001. Very serious vulnerability'
    scenario: str = 'UNAUTHORIZED_USER_EXTRANET'
    actor: str = 'ANYONE_INTERNET'
    description: str = 'I just have updated the description'
    requirements: str = 'REQ.0132. Passwords (phrase type) must be at least 3 words long.'
    attack_vector_desc: str = 'This is an updated attack vector'
    threat: str = 'Updated threat'
    recommendation: str = 'Updated recommendation'
    affected_systems: str = 'Server bWAPP'
    records: str = 'Clave plana'
    records_number: int = 12
    cwe: str = '200'
    risk: str = 'This is pytest created draft'
    finding_type: str = 'SECURITY'
    observation_content: str = "This is a observation test"
    consult_content: str = "This is a comenting test"
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding=finding_id,
    )
    assert 'errors' not in result
    vuln_ids: List[str] = [vuln['id'] for vuln in result['data']['finding']['vulnerabilities']]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result['data']['finding']['openVulnerabilities'] == 1
    assert result['data']['finding']['closedVulnerabilities'] == 1
    assert len(result['data']['finding']['evidence']) == 7
    assert result['data']['finding']['evidence']['evidence2']['url'] == ''
    assert f'group1-{finding_id}' in result['data']['finding']['evidence']['animation']['url']
    assert result['data']['finding']['title'] == title
    assert result['data']['finding']['scenario'] == scenario
    assert result['data']['finding']['actor'] == actor
    assert result['data']['finding']['description'] == description
    assert result['data']['finding']['requirements'] == requirements
    assert result['data']['finding']['attackVectorDesc'] == attack_vector_desc
    assert result['data']['finding']['threat'] == threat
    assert result['data']['finding']['recommendation'] == recommendation
    assert result['data']['finding']['affectedSystems'] == affected_systems
    assert result['data']['finding']['compromisedAttributes'] == records
    assert result['data']['finding']['compromisedRecords'] == records_number
    assert result['data']['finding']['cweUrl'] == cwe
    assert result['data']['finding']['btsUrl'] == ''
    assert result['data']['finding']['risk'] == risk
    assert result['data']['finding']['type'] == finding_type
    assert result['data']['finding']['observations'] == []
    assert result['data']['finding']['consulting'] == []


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('finding')
async def test_analyst(populate: bool):
    assert populate
    open_vuln: str = '6401bc87-8633-4a4a-8d8e-7dae0ca57e6a'
    closed_vuln: str = 'be09edb7-cd5c-47ed-bee4-97c645acdce8'
    finding_id: str = '475041513'
    title: str = 'F001. Very serious vulnerability'
    scenario: str = 'UNAUTHORIZED_USER_EXTRANET'
    actor: str = 'ANYONE_INTERNET'
    description: str = 'I just have updated the description'
    requirements: str = 'REQ.0132. Passwords (phrase type) must be at least 3 words long.'
    attack_vector_desc: str = 'This is an updated attack vector'
    threat: str = 'Updated threat'
    recommendation: str = 'Updated recommendation'
    affected_systems: str = 'Server bWAPP'
    records: str = 'Clave plana'
    records_number: int = 12
    cwe: str = '200'
    risk: str = 'This is pytest created draft'
    finding_type: str = 'SECURITY'
    observation_content: str = "This is a observation test"
    consult_content: str = "This is a comenting test"
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding=finding_id,
    )
    assert 'errors' not in result
    vuln_ids: List[str] = [vuln['id'] for vuln in result['data']['finding']['vulnerabilities']]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result['data']['finding']['openVulnerabilities'] == 1
    assert result['data']['finding']['closedVulnerabilities'] == 1
    assert len(result['data']['finding']['evidence']) == 7
    assert result['data']['finding']['evidence']['evidence2']['url'] == ''
    assert f'group1-{finding_id}' in result['data']['finding']['evidence']['animation']['url']
    assert result['data']['finding']['title'] == title
    assert result['data']['finding']['scenario'] == scenario
    assert result['data']['finding']['actor'] == actor
    assert result['data']['finding']['description'] == description
    assert result['data']['finding']['requirements'] == requirements
    assert result['data']['finding']['attackVectorDesc'] == attack_vector_desc
    assert result['data']['finding']['threat'] == threat
    assert result['data']['finding']['recommendation'] == recommendation
    assert result['data']['finding']['affectedSystems'] == affected_systems
    assert result['data']['finding']['compromisedAttributes'] == records
    assert result['data']['finding']['compromisedRecords'] == records_number
    assert result['data']['finding']['cweUrl'] == cwe
    assert result['data']['finding']['btsUrl'] == ''
    assert result['data']['finding']['risk'] == risk
    assert result['data']['finding']['type'] == finding_type
    assert result['data']['finding']['observations'] == []
    assert result['data']['finding']['consulting'] == []
