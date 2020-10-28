import os
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from backend.utils import datetime as datetime_utils
from test_async.functional_test.reviewer.utils import get_result

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
    title = 'FIN.S.0001. Very serious vulnerability'
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
    result = await get_result(data)
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
    result = await get_result(data)
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
    result = await get_result(data)
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
        result = await get_result(data, stakeholder='integratesmanager@gmail.com')
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']

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
    result = await get_result(data)
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
            rejectDraft(findingId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['rejectDraft']
    assert result['data']['rejectDraft']['success']

    query = f'''
        mutation {{
            approveDraft(draftId: "{draft_id}") {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['approveDraft']['success']

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
    result = await get_result(data)
    assert 'errors' not in result
    group_findings = result['data']['project']['findings']
    finding_ids = [finding['id'] for finding in group_findings]
    assert finding_id in finding_ids
