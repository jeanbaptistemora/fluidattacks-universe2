import os
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from backend.utils import datetime as datetime_utils
from test_async.functional_test.executive.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_finding():
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
    title = 'FIN.S.0001. Very serious closer vulnerability'
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
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    assert 'success' in result['data']['createDraft']
    assert result['data']['createDraft']['success']

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
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    draft = [draft for draft in result['data']['project']['drafts'] if draft['title'] == title][0]
    draft_id = draft['id']

    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../mock/test-vulns.yaml')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='text/x-yaml')
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
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    assert result['data']['uploadFile']['success']

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
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    assert 'success' in result['data']['updateSeverity']
    assert result['data']['updateSeverity']['success']

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
    filename = os.path.join(filename, '../../mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='image/gif')
        variables = {
            'evidenceId': 'EVIDENCE2',
            'findingId': draft_id,
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}
        result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']

    evidence2_description = 'this is a evidence2 description'
    query = f'''
        mutation {{
            updateEvidenceDescription(
                description: "{evidence2_description}",
                findingId: "{draft_id}",
                evidenceId: EVIDENCE2
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']

    query = f'''
        mutation {{
            submitDraft(findingId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesanalyst@fluidattacks.com')
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']

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

    finding_id = draft_id
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
            historicTreatment
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
            pendingVulns {{
                analyst
                currentApprovalStatus
                currentState
                findingId
                historicState
                historicVerification {{
                    status
                }}
                id
                lastAnalyst
                lastApprovedStatus
                remediated
                severity
                source
                specific
                tag
                tags
                treatmentManager
                verification
                vulnType
                where
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
    assert result['data']['finding']['tracking'] == [{'closed': 2, 'cycle': 0, 'date': today, 'effectiveness': 66, 'open': 1}]
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
    assert result['data']['finding']['evidence']['evidence2']['description'] == evidence2_description
    assert f'unittesting-{finding_id}' in result['data']['finding']['evidence']['evidence2']['url']
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
    assert result['data']['finding']['pendingVulns'] == []
    historic_treatment = result['data']['finding']['historicTreatment']
    for index in range(len(historic_treatment)):
        historic_treatment[index]['date'] = (
            historic_treatment[index]['date'][:-9]
        )
    assert historic_treatment == [
        {
            'date': today,
            'treatment': 'NEW',
            'user': 'integratesanalyst@fluidattacks.com'
        }
    ]
