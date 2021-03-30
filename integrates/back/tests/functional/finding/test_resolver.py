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
    identifier: str = '475041513'
    project_name: str = 'group1'
    release_date: str = '2018-04-07 19:45:11'
    severity: Dict[str, float] = {
        'attackComplexity': 0.44,
        'attackVector': 0.2,
        'availabilityImpact': 0.22,
        'availabilityRequirement': 1.5,
        'confidentialityImpact': 0.22,
        'confidentialityRequirement': 0.5,
        'exploitability': 0.94,
        'integrityImpact': 0.22,
        'integrityRequirement': 1.0,
        'modifiedAttackComplexity': 0.44,
        'modifiedAttackVector': 0.85,
        'modifiedAvailabilityImpact': 0.22,
        'modifiedConfidentialityImpact': 0.22,
        'modifiedIntegrityImpact': 0.0,
        'modifiedPrivilegesRequired': 0.27,
        'modifiedUserInteraction': 0.62,
        'modifiedSeverityScope': 0.0,
        'privilegesRequired': 0.62,
        'remediationLevel': 0.95,
        'reportConfidence': 1.0,
        'severityScope': 1.2,
        'userInteraction': 0.85
    }
    cvss_version: str = '3.1'
    state: str = 'open'
    last_vuln: int = 1087
    remediated: bool = False
    age: int = 1087
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = ''
    historic_state: List[Any] = [
        {
            'date': '2018-04-07 19:45:11',
            'analyst': 'test1@gmail.com',
            'source': 'source_path',
            'state': 'APPROVED'
        }
    ]
    current_state: str = 'APPROVED'
    new_remediated: bool = False
    verified: bool = True
    analyst: str = 'test1@gmail.com'
    ports_vulns: List[Any] = [
        {
            'specific': '2321'
        },
        {
            'specific': '9999'
        }
    ]
    inputs_vulns: List[Any] = []
    lines_vulns: List[Any] = []
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
    tracking: Dict[str, Any] =  {
        'tracking': [
            {
                'cycle': 0,
                'open': 1,
                'closed': 0,
                'date': '2018-04-07',
                'accepted': 0,
                'accepted_undefined': 0,
                'manager': '',
                'justification': ''
            },
            {
                'cycle': 1,
                'open': 0,
                'closed': 1,
                'date': '2018-04-07',
                'accepted': 0,
                'accepted_undefined': 0,
                'manager': '',
                'justification': ''
            },
            {
                'cycle': 2,
                'open': 0,
                'closed': 0,
                'date': '2018-04-08',
                'accepted': 1,
                'accepted_undefined': 0,
                'manager': 'anything@gmail.com',
                'justification': 'justification'
            }
        ]
    }
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding=finding_id,
    )
    assert 'errors' not in result
    assert result['data']['finding']['id'] == identifier
    assert result['data']['finding']['projectName'] == project_name
    assert result['data']['finding']['releaseDate'] == release_date
    assert result['data']['finding']['severity'] == severity
    assert result['data']['finding']['cvssVersion'] == cvss_version
    assert result['data']['finding']['state'] == state
    assert result['data']['finding']['lastVulnerability'] == last_vuln
    assert result['data']['finding']['remediated'] == remediated
    assert result['data']['finding']['age'] == age
    assert result['data']['finding']['isExploitable'] == is_exploitable
    assert result['data']['finding']['severityScore'] == severity_score
    assert result['data']['finding']['reportDate'] == report_date
    assert result['data']['finding']['historicState'] == historic_state
    assert result['data']['finding']['currentState'] == current_state
    assert result['data']['finding']['newRemediated'] == new_remediated
    assert result['data']['finding']['verified'] == verified
    assert result['data']['finding']['analyst'] == analyst
    assert result['data']['finding']['portsVulns'] == ports_vulns 
    assert result['data']['finding']['inputsVulns'] == inputs_vulns 
    assert result['data']['finding']['linesVulns'] == lines_vulns 
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
    assert result['data']['finding']['tracking'] == tracking.get('tracking')


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('finding')
async def test_analyst(populate: bool):
    assert populate
    identifier: str = '475041513'
    project_name: str = 'group1'
    release_date: str = '2018-04-07 19:45:11'
    severity: Dict[str, float] = {
        'attackComplexity': 0.44,
        'attackVector': 0.2,
        'availabilityImpact': 0.22,
        'availabilityRequirement': 1.5,
        'confidentialityImpact': 0.22,
        'confidentialityRequirement': 0.5,
        'exploitability': 0.94,
        'integrityImpact': 0.22,
        'integrityRequirement': 1.0,
        'modifiedAttackComplexity': 0.44,
        'modifiedAttackVector': 0.85,
        'modifiedAvailabilityImpact': 0.22,
        'modifiedConfidentialityImpact': 0.22,
        'modifiedIntegrityImpact': 0.0,
        'modifiedPrivilegesRequired': 0.27,
        'modifiedUserInteraction': 0.62,
        'modifiedSeverityScope': 0.0,
        'privilegesRequired': 0.62,
        'remediationLevel': 0.95,
        'reportConfidence': 1.0,
        'severityScope': 1.2,
        'userInteraction': 0.85
    }
    cvss_version: str = '3.1'
    state: str = 'open'
    last_vuln: int = 1087
    remediated: bool = False
    age: int = 1087
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = ''
    historic_state: List[Any] = [
        {
            'date': '2018-04-07 19:45:11',
            'analyst': 'test1@gmail.com',
            'source': 'source_path',
            'state': 'APPROVED'
        }
    ]
    current_state: str = 'APPROVED'
    new_remediated: bool = False
    verified: bool = True
    analyst: str = 'test1@gmail.com'
    ports_vulns: List[Any] = [
        {
            'specific': '2321'
        },
        {
            'specific': '9999'
        }
    ]
    inputs_vulns: List[Any] = []
    lines_vulns: List[Any] = []
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
    tracking: Dict[str, Any] =  {
        'tracking': [
            {
                'cycle': 0,
                'open': 1,
                'closed': 0,
                'date': '2018-04-07',
                'accepted': 0,
                'accepted_undefined': 0,
                'manager': '',
                'justification': ''
            },
            {
                'cycle': 1,
                'open': 0,
                'closed': 1,
                'date': '2018-04-07',
                'accepted': 0,
                'accepted_undefined': 0,
                'manager': '',
                'justification': ''
            },
            {
                'cycle': 2,
                'open': 0,
                'closed': 0,
                'date': '2018-04-08',
                'accepted': 1,
                'accepted_undefined': 0,
                'manager': 'anything@gmail.com',
                'justification': 'justification'
            }
        ]
    }
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding=finding_id,
    )
    assert 'errors' not in result
    assert result['data']['finding']['id'] == identifier
    assert result['data']['finding']['projectName'] == project_name
    assert result['data']['finding']['releaseDate'] == release_date
    assert result['data']['finding']['severity'] == severity
    assert result['data']['finding']['cvssVersion'] == cvss_version
    assert result['data']['finding']['state'] == state
    assert result['data']['finding']['lastVulnerability'] == last_vuln
    assert result['data']['finding']['remediated'] == remediated
    assert result['data']['finding']['age'] == age
    assert result['data']['finding']['isExploitable'] == is_exploitable
    assert result['data']['finding']['severityScore'] == severity_score
    assert result['data']['finding']['reportDate'] == report_date
    assert result['data']['finding']['historicState'] == historic_state
    assert result['data']['finding']['currentState'] == current_state
    assert result['data']['finding']['newRemediated'] == new_remediated
    assert result['data']['finding']['verified'] == verified
    assert result['data']['finding']['analyst'] == analyst
    assert result['data']['finding']['portsVulns'] == ports_vulns 
    assert result['data']['finding']['inputsVulns'] == inputs_vulns 
    assert result['data']['finding']['linesVulns'] == lines_vulns
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
    assert result['data']['finding']['tracking'] == tracking.get('tracking')
