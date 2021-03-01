# Standard libraries
import os
import pytest

# Third party libraries
from starlette.datastructures import UploadFile

# Local libraries
from backend.api import get_new_context
from backend.exceptions import VulnNotFound
from backend.utils import datetime as datetime_utils
from test_functional.analyst.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_finding():
    context = get_new_context()
    today = datetime_utils.get_as_str(
        datetime_utils.get_now(),
        date_format='%Y-%m-%d'
    )
    cwe = '200'
    description = 'This is pytest created draft'
    group_name = 'unittesting'
    recommendation = 'Solve this finding'
    requirements = 'REQ.0001. Apply filters'
    risk = 'This is pytest created draft'
    threat = 'Attacker'
    title = 'F001. Very serious vulnerability'
    draft_type = 'SECURITY'
    query = f'''
        mutation {{
            createDraft(
                cwe: "{cwe}",
                description: "{description}",
                projectName: "{group_name}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                risk: "{risk}",
                threat: "{threat}",
                title: "{title}",
                type: {draft_type}
            ) {{
                success
            }}
        }}

    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['createDraft']
    assert result['data']['createDraft']['success']

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                drafts {{
                    id
                    age
                    title
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    draft = [draft for draft in result['data']['project']['drafts'] if draft['title'] == title][0]
    draft_id = draft['id']

    context = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../test_unit/mock/test-vulns.yaml')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'text/x-yaml')
        query = '''
            mutation UploadFileMutation(
                $file: Upload!, $findingId: String!
            ) {
                uploadFile (
                    file: $file,
                    findingId: $findingId
                ) {
                    success
                }
            }
        '''
        variables = {
            'file': uploaded_file,
            'findingId': draft_id,
        }
        data = {'query': query, 'variables': variables}
        result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['uploadFile']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            updateSeverity (
            findingId: "{draft_id}",
            data: {{
                attackComplexity: 0.77, attackVector: 0.62,
                availabilityImpact: "0", availabilityRequirement: "1",
                confidentialityImpact: "0", confidentialityRequirement: "1",
                cvssVersion: "3.1", exploitability: 0.91, id: "{draft_id}",
                integrityImpact: "0.22", integrityRequirement: "1",
                modifiedAttackComplexity: 0.77, modifiedAttackVector: 0.62,
                modifiedAvailabilityImpact: "0",
                modifiedConfidentialityImpact: "0",
                modifiedIntegrityImpact: "0.22",
                modifiedPrivilegesRequired: "0.62",
                modifiedSeverityScope: 0, modifiedUserInteraction: 0.85,
                privilegesRequired: "0.62", remediationLevel: "0.97",
                reportConfidence: "0.92",
                severity: "2.9", severityScope: 0, userInteraction: 0.85
            }}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['updateSeverity']
    assert result['data']['updateSeverity']['success']

    context = get_new_context()
    query = '''
        mutation UpdateEvidenceMutation(
            $evidenceId: EvidenceType!, $file: Upload!, $findingId: String!
        ) {
            updateEvidence(
                evidenceId: $evidenceId, file: $file, findingId: $findingId
            ) {
                success
            }
        }
    '''
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../test_unit/mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'image/gif')
        variables = {
            'evidenceId': 'ANIMATION',
            'findingId': draft_id,
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}
        result = await get_result(data, context=context)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']

    context = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../test_unit/mock/test-img.png')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'image/png')
        variables = {
            'evidenceId': 'EVIDENCE2',
            'findingId': draft_id,
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}
        result = await get_result(data, context=context)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']

    context = get_new_context()
    evidence_description = 'this is a test description'
    query = f'''
        mutation {{
                updateEvidenceDescription(
                description: "{evidence_description}",
                findingId: "{draft_id}",
                evidenceId: EVIDENCE2
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            submitDraft(findingId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            rejectDraft(findingId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['rejectDraft']
    assert result['data']['rejectDraft']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            submitDraft(findingId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            approveDraft(draftId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert result['data']['approveDraft']['success']

    context = get_new_context()
    finding_id = draft_id
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                findings {{
                    id
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    group_findings = result['data']['project']['findings']
    finding_ids = [finding['id'] for finding in group_findings]
    assert finding_id in finding_ids

    context = get_new_context()
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
            historicState
            currentState
            newRemediated
            verified
            closedVulns: vulnerabilities(state: "closed") {{
                id
            }}
            openVulns: vulnerabilities(state: "open") {{
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
    assert result['data']['finding']['id'] == finding_id
    assert result['data']['finding']['projectName'] == group_name
    result['data']['finding']['releaseDate'] = (
        result['data']['finding']['releaseDate'][:-9]
    )
    assert result['data']['finding']['releaseDate'] == today
    assert result['data']['finding']['openVulnerabilities'] == 1
    assert result['data']['finding']['closedVulnerabilities'] == 2
    assert result['data']['finding']['tracking'] == [{
        'accepted': 0, 'accepted_undefined': 0, 'closed': 2, 'cycle': 0, 'date': today,
        'justification': '', 'manager': '', 'open': 0},
        {'accepted': 0, 'accepted_undefined': 0, 'closed': 0, 'cycle': 1, 'date': today,
         'justification': '', 'manager': '', 'open': 1
    }]
    assert result['data']['finding']['records'] == '[]'
    assert result['data']['finding']['severity'] == {
        'attackComplexity': 0.77,
        'attackVector': 0.62,
        'availabilityImpact': 0.0,
        'availabilityRequirement': 1.0,
        'confidentialityImpact': 0.0,
        'confidentialityRequirement': 1.0,
        'exploitability': 0.91,
        'integrityImpact': 0.22,
        'integrityRequirement': 1.0,
        'modifiedAttackComplexity': 0.77,
        'modifiedAttackVector': 0.62,
        'modifiedAvailabilityImpact': 0.0,
        'modifiedConfidentialityImpact': 0.0,
        'modifiedIntegrityImpact': 0.22,
        'modifiedPrivilegesRequired': 0.62,
        'modifiedSeverityScope': 0.0,
        'modifiedUserInteraction': 0.85,
        'privilegesRequired': 0.62,
        'remediationLevel': 0.97,
        'reportConfidence': 0.92,
        'severityScope': 0.0,
        'userInteraction': 0.85
    }
    assert result['data']['finding']['cvssVersion'] == '3.1'
    assert result['data']['finding']['exploit'] == ''
    assert len(result['data']['finding']['evidence']) == 7
    assert result['data']['finding']['evidence']['evidence2']['description'] == evidence_description
    assert f'unittesting-{finding_id}' in result['data']['finding']['evidence']['animation']['url']
    assert result['data']['finding']['state'] == 'open'
    assert result['data']['finding']['title'] == title
    assert result['data']['finding']['scenario'] == ''
    assert result['data']['finding']['actor'] == ''
    assert result['data']['finding']['description'] == description
    assert result['data']['finding']['requirements'] == requirements
    assert result['data']['finding']['attackVectorDesc'] == ''
    assert result['data']['finding']['threat'] == threat
    assert result['data']['finding']['recommendation'] == recommendation
    assert result['data']['finding']['affectedSystems'] == ''
    assert result['data']['finding']['compromisedAttributes'] == ''
    assert result['data']['finding']['compromisedRecords'] == 0
    assert result['data']['finding']['cweUrl'] == cwe
    assert result['data']['finding']['btsUrl'] == ''
    assert result['data']['finding']['risk'] == risk
    assert result['data']['finding']['remediated'] == False
    assert result['data']['finding']['type'] == draft_type
    assert result['data']['finding']['isExploitable'] == False
    assert result['data']['finding']['severityScore'] == 2.9
    result['data']['finding']['reportDate'] = (
        result['data']['finding']['reportDate'][:-9]
    )
    assert result['data']['finding']['reportDate'] == today
    assert result['data']['finding']['currentState'] == 'APPROVED'
    assert result['data']['finding']['newRemediated'] == False
    assert result['data']['finding']['verified'] == True
    assert result['data']['finding']['analyst'] == 'integratesanalyst@fluidattacks.com'
    assert result['data']['finding']['observations'] == []
    historic_state = result['data']['finding']['historicState']
    for index in range(len(historic_state)):
        historic_state[index]['date'] = (
            historic_state[index]['date'][:-9]
        )
    assert historic_state == [
        {
            'analyst': 'integratesanalyst@fluidattacks.com',
            'date': today,
            'source': 'integrates',
            'state': 'CREATED'
        },
        {
            'analyst': 'integratesanalyst@fluidattacks.com',
            'date': today,
            'source': 'integrates',
            'state': 'SUBMITTED'
        },
        {
            'analyst': 'integratesanalyst@fluidattacks.com',
            'date': today,
            'source': 'integrates',
            'state': 'REJECTED'
        },
        {
            'analyst': 'integratesanalyst@fluidattacks.com',
            'date': today,
            'source': 'integrates',
            'state': 'SUBMITTED'
        },
        {
            'analyst': 'integratesmanager@gmail.com',
            'date': today,
            'source': 'integrates',
            'state': 'APPROVED'
        }
    ]

    context = get_new_context()
    open_vulnerabilities = result['data']['finding']['openVulns']
    closed_vulnerabilities = result['data']['finding']['closedVulns']
    vuln_ids = [vuln['id'] for vuln in open_vulnerabilities + closed_vulnerabilities]
    actor = 'ANYONE_INTERNET'
    affected_systems = 'Server bWAPP'
    attack_vector_desc = 'This is an updated attack vector'
    records = 'Clave plana'
    records_number = 12
    cwe = '200'
    description = 'I just have updated the description'
    recommendation = 'Updated recommendation'
    requirements = 'REQ.0132. Passwords (phrase type) must be at least 3 words long.'
    scenario = 'UNAUTHORIZED_USER_EXTRANET'
    threat = 'Updated threat'
    title = 'F051. Weak passwords reversed'
    finding_type = 'SECURITY'
    query = f'''
        mutation {{
            updateDescription(
                actor: "{actor}",
                affectedSystems: "{affected_systems}",
                attackVectorDesc: "{attack_vector_desc}",
                cwe: "{cwe}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                recordsNumber: {records_number},
                requirements: "{requirements}",
                scenario: "{scenario}",
                threat: "{threat}",
                title: "{title}",
                findingType: "{finding_type}"
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['updateDescription']
    assert result['data']['updateDescription']['success']

    context = get_new_context()
    query = f'''
        mutation {{
            removeEvidence(evidenceId: EVIDENCE2, findingId: "{finding_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query, 'variables': variables}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['removeEvidence']['success']

    context = get_new_context()
    observation_content = "This is a observation test"
    query = f'''
        mutation {{
            addFindingConsult(
                content: "{observation_content}",
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
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['addFindingConsult']
    assert result['data']['addFindingConsult']['success']

    context = get_new_context()
    consult_content = "This is a comenting test"
    query = f'''
        mutation {{
            addFindingConsult(
                content: "{consult_content}",
                findingId: "{finding_id}",
                type: CONSULT,
                parent: "0"
            ) {{
                success
                commentId
            }}
        }}
        '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['addFindingConsult']
    assert result['data']['addFindingConsult']['success']

    context = get_new_context()
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            consulting {{
                content
            }}
            records
            evidence
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
            type
            observations{{
                content
                email
            }}
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert len(result['data']['finding']['evidence']) == 7
    assert result['data']['finding']['evidence']['evidence2']['description'] == ''
    assert result['data']['finding']['evidence']['evidence2']['url'] == ''
    assert f'unittesting-{finding_id}' in result['data']['finding']['evidence']['animation']['url']
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
    assert result['data']['finding']['observations'] == [
        {
            'content': observation_content,
            'email': 'integratesanalyst@fluidattacks.com'
        }
    ]
    assert result['data']['finding']['consulting'] == [{'content': consult_content}]

    context = get_new_context()
    vuln_query = '''
        query GetVulnInfo($vuln1Id: String!, $vuln2Id: String!, $vuln3Id: String!) {
            vuln1: vulnerability(uuid: $vuln1Id) {
                currentState
            }
            vuln2: vulnerability(uuid: $vuln2Id) {
                currentState
            }
            vuln3: vulnerability(uuid: $vuln3Id) {
                currentState
            }
        }
    '''
    variables = {'vuln1Id': vuln_ids[0], 'vuln2Id': vuln_ids[1], 'vuln3Id': vuln_ids[2]}
    data = {'query': vuln_query, 'variables': variables}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['vuln1']['currentState'] == 'open'
    assert result['data']['vuln2']['currentState'] == 'closed'
    assert result['data']['vuln3']['currentState'] == 'closed'

    context = get_new_context()
    query = f'''
        mutation {{
            deleteFinding(findingId: "{finding_id}", justification: NOT_REQUIRED) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['deleteFinding']
    assert result['data']['deleteFinding']['success']

    context = get_new_context()
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                findings {{
                    id
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    group_findings = result['data']['project']['findings']
    finding_ids = [finding['id'] for finding in group_findings]
    assert finding_id not in finding_ids

    variables = {'vuln1Id': vuln_ids[0], 'vuln2Id': vuln_ids[1], 'vuln3Id': vuln_ids[2]}
    data = {'query': vuln_query, 'variables': variables}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(VulnNotFound())
    assert result['errors'][1]['message'] == str(VulnNotFound())
    assert result['errors'][2]['message'] == str(VulnNotFound())
