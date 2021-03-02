import pytest

from backend.utils import datetime as datetime_utils
from back.tests.functional.group_manager.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_finding():
    finding_id = '463558592'
    expected_output =  {
        'id': finding_id,
        'project_name': 'unittesting',
        'release_date': '2018-12-17 00:00:00',
        'open_vulnerabilities': 1,
        'closed_vulnerabilities': 1,
        'tracking': [
            {
                'cycle': 0,
                'open': 1,
                'closed': 0,
                'date': '2019-01-15',
                'accepted': 0,
                'accepted_undefined': 0,
                'justification': '',
                'manager': '',
            },
            {
                'cycle': 1,
                'open': 0,
                'closed': 1,
                'date': '2019-01-15',
                'accepted': 0,
                'accepted_undefined': 0,
                'justification': '',
                'manager': '',
            },
            {
                'cycle': 2,
                'open': 0,
                'closed': 0,
                'date': '2019-01-15',
                'justification': 'This is a treatment justification test',
                'accepted': 1,
                'accepted_undefined': 0,
                'manager': 'integratesuser@gmail.com',
            }
        ],
        'records': '[]',
        'severity': {
            'attackComplexity': 0.44,
            'attackVector': 0.62,
            'availabilityImpact': 0.0,
            'availabilityRequirement': 1.0,
            'confidentialityImpact': 0.56,
            'confidentialityRequirement': 1.0,
            'exploitability': 0.91,
            'integrityImpact': 0.22,
            'integrityRequirement': 1.5,
            'modifiedAttackComplexity': 0.44,
            'modifiedAttackVector': 0.62,
            'modifiedAvailabilityImpact': 0.0,
            'modifiedConfidentialityImpact': 0.56,
            'modifiedIntegrityImpact': 0.22,
            'modifiedPrivilegesRequired': 0.62,
            'modifiedUserInteraction': 0.62,
            'modifiedSeverityScope': 0.0,
            'privilegesRequired': 0.62,
            'remediationLevel': 0.95,
            'reportConfidence': 0.96,
            'severityScope': 0.0,
            'userInteraction': 0.62
        },
        'cvss_version': '3.1',
        'exploit': '',
        'evidence': {
            'animation': {
                'url': '',
                'description': ''
            },
            'evidence1': {
                'date': '2018-12-17 00:00:00',
                'url': 'unittesting-463558592-evidence_route_1.png',
                'description': 'test'
            },
            'evidence2': {
                'date': '2018-12-17 00:00:00',
                'url': 'unittesting-463558592-evidence_route_2.jpg',
                'description': 'Test2'
            },
            'evidence3': {
                'date': '2018-12-17 00:00:00',
                'url': 'unittesting-463558592-evidence_route_3.png',
                'description': 'Test3'
            },
            'evidence4': {
                'date': '2018-12-17 00:00:00',
                'url': 'unittesting-463558592-evidence_route_4.png',
                'description': 'An error'
            },
            'evidence5': {
                'date': '2018-12-17 00:00:00',
                'url': 'unittesting-463558592-evidence_route_5.png',
                'description': '4'
            },
            'exploitation': {
                'url': '',
                'description': ''
            }
        },
        'state': 'open',
        'title': 'F007. Cross site request forgery',
        'scenario': 'AUTHORIZED_USER_EXTRANET',
        'actor': 'ANY_COSTUMER',
        'description': 'La aplicación permite engañar a un usuario autenticado por medio de links manipulados para ejecutar acciones sobre la aplicación sin su consentimiento..',
        'requirements': 'REQ.0174. La aplicación debe garantizar que las peticiones que ejecuten transacciones no sigan un patrón discernible.',
        'attack_vector_desc': 'test',
        'threat': 'Test.',
        'recommendation': 'Hacer uso de tokens en los formularios para la verificación de las peticiones realizadas por usuarios legítimos.\r\n',
        'affected_systems': 'test',
        'compromised_attributes': '',
        'compromised_records': 0,
        'cwe_url': '200',
        'bts_url': '',
        'risk': '',
        'remediated': False,
        'type': 'SECURITY',
        'is_exploitable': False,
        'severity_score': 4.3,
        'report_date': '2018-04-07 19:45:11',
        'current_state': 'APPROVED',
        'new_remediated': False,
        'verified': True,
        'vulnerabilities': [
            {
                'id': '0a848781-b6a4-422e-95fa-692151e6a98e'
            },
            {
                'id': '242f848c-148a-4028-8e36-c7d995502590'
            },
        ],
        'ports_vulns': [],
        'inputs_vulns': [],
        'lines_vulns': [
            {
                'specific': '12'
            },
            {
                'specific': '12456'
            },
            {
                'specific': '345'
            },
            {
                'specific': '564'
            },
            {
                'specific': '123345'
            },
            {
                'specific': '123'
            }
        ],
        'analyst': 'unittest@fluidattacks.com',
        'observations': [],
        '__typename': 'Finding'
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
            projectName
            releaseDate
            openVulnerabilities
            closedVulnerabilities
            tracking
            records
            severity
            cvssVersion
            exploit
            evidence
            state
            lastVulnerability
            title
            scenario
            actor
            description
            requirements
            attackVectorDesc
            threat
            recommendation
            affectedSystems
            compromisedAttributes
            compromisedRecords
            cweUrl
            btsUrl
            risk
            remediated
            type
            age
            isExploitable
            severityScore
            reportDate
            currentState
            newRemediated
            verified
            vulnerabilities {{
                id
            }}
            portsVulns {{
                specific
            }}
            inputsVulns {{
                specific
            }}
            linesVulns {{
                specific
            }}
            analyst
            observations{{
                content
                email
            }}
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['finding']['id'] == expected_output.get('id')
    assert result['data']['finding']['projectName'] == expected_output.get('project_name')
    assert result['data']['finding']['releaseDate'] == expected_output.get('release_date')
    assert result['data']['finding']['openVulnerabilities'] == expected_output.get('open_vulnerabilities')
    assert result['data']['finding']['closedVulnerabilities'] == expected_output.get('closed_vulnerabilities')
    assert result['data']['finding']['tracking'] == expected_output.get('tracking')
    assert result['data']['finding']['records'] == expected_output.get('records')
    assert result['data']['finding']['severity'] == expected_output.get('severity')
    assert result['data']['finding']['cvssVersion'] == expected_output.get('cvss_version')
    assert result['data']['finding']['exploit'] == expected_output.get('exploit')
    assert result['data']['finding']['evidence'] == expected_output.get('evidence')
    assert result['data']['finding']['state'] == expected_output.get('state')
    assert result['data']['finding']['title'] == expected_output.get('title')
    assert result['data']['finding']['scenario'] == expected_output.get('scenario')
    assert result['data']['finding']['actor'] == expected_output.get('actor')
    assert result['data']['finding']['description'] == expected_output.get('description')
    assert result['data']['finding']['requirements'] == expected_output.get('requirements')
    assert result['data']['finding']['attackVectorDesc'] == expected_output.get('attack_vector_desc')
    assert result['data']['finding']['threat'] == expected_output.get('threat')
    assert result['data']['finding']['recommendation'] == expected_output.get('recommendation')
    assert result['data']['finding']['affectedSystems'] == expected_output.get('affected_systems')
    assert result['data']['finding']['compromisedAttributes'] == expected_output.get('compromised_attributes')
    assert result['data']['finding']['compromisedRecords'] == expected_output.get('compromised_records')
    assert result['data']['finding']['cweUrl'] == expected_output.get('cwe_url')
    assert result['data']['finding']['btsUrl'] == expected_output.get('bts_url')
    assert result['data']['finding']['risk'] == expected_output.get('risk')
    assert result['data']['finding']['remediated'] == expected_output.get('remediated')
    assert result['data']['finding']['type'] == expected_output.get('type')
    assert result['data']['finding']['isExploitable'] == expected_output.get('is_exploitable')
    assert result['data']['finding']['severityScore'] == expected_output.get('severity_score')
    assert result['data']['finding']['reportDate'] == expected_output.get('report_date')
    assert result['data']['finding']['currentState'] == expected_output.get('current_state')
    assert result['data']['finding']['newRemediated'] == expected_output.get('new_remediated')
    assert result['data']['finding']['verified'] == expected_output.get('verified')
    assert result['data']['finding']['vulnerabilities'] == expected_output.get('vulnerabilities')
    assert result['data']['finding']['portsVulns'] == expected_output.get('ports_vulns')
    assert result['data']['finding']['inputsVulns'] == expected_output.get('inputs_vulns')
    assert result['data']['finding']['linesVulns'] == expected_output.get('lines_vulns')
    assert result['data']['finding']['analyst'] == expected_output.get('analyst')
    assert result['data']['finding']['observations'] == expected_output.get('observations')

    consult_content = "This is a observation test"
    query = f'''
        mutation {{
            addFindingConsult(
                content: "{consult_content}",
                findingId: "{finding_id}",
                type: OBSERVATION,
                parent: "0"
            ) {{
                success
                commentId
            }}
        }}
        '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addFindingConsult']
    assert result['data']['addFindingConsult']['success']

    expected_output = {
        'consulting': {
            'content': consult_content
        },
        'observations':  [
            {
                'content': consult_content,
                'email': 'unittest2@fluidattacks.com'
            }
        ],
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            consulting {{
                content
            }}
            observations{{
                content
                email
            }}
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  expected_output.get('consulting') not in result['data']['finding']['consulting']
    assert result['data']['finding']['observations'] == expected_output.get('observations')
