from collections import OrderedDict
import json
import os
import pytest

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from graphql import GraphQLError
from jose import jwt
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.domain.finding import get_finding
from backend.exceptions import FindingNotFound, NotVerificationRequested

pytestmark = pytest.mark.asyncio

class FindingTests(TestCase):

    async def _get_result(self, data, user='integratesmanager@gmail.com'):
        """Get result."""
        request = RequestFactory().post('/',
                                        {'data': 'finding(identifier: "422286126")'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': user,
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.loaders = {
            'finding': FindingLoader(),
            'project': ProjectLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    @pytest.mark.no_changes_db
    async def test_finding(self):
        """Check for finding query."""
        query = '''{
          finding(identifier: "422286126"){
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
              comments {
                  id
                  content
              }
              observations {
                  id
                  content
              }
              state
              lastVulnerability
              historicState
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
              analyst
              historicTreatment
              currentState
              newRemediated
              verified
              vulnerabilities {
                specific
              }
              portsVulns {
                  specific
              }
              inputsVulns {
                  specific
              }
              linesVulns {
                  specific
              }
              pendingVulns {
                  specific
              }
              __typename
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert result['data']['finding']['id'] == '422286126'
        assert result['data']['finding']['projectName'] == 'unittesting'
        assert result['data']['finding']['openVulnerabilities'] == 1
        assert result['data']['finding']['closedVulnerabilities'] == 0
        assert result['data']['finding']['releaseDate'] == '2018-07-09 00:00:00'
        assert result['data']['finding']['tracking'][0]['cycle'] == 0
        assert result['data']['finding']['tracking'][0]['open'] == 1
        assert result['data']['finding']['tracking'][0]['closed'] == 0
        assert result['data']['finding']['tracking'][0]['effectiveness'] == 0
        assert result['data']['finding']['tracking'][0]['date'] == '2018-09-28'
        assert 'records' in result['data']['finding']
        assert result['data']['finding']['severity']['attackComplexity'] == 0.77
        assert result['data']['finding']['severity']['remediationLevel'] == 0.97
        assert result['data']['finding']['cvssVersion'] == "3.1"
        assert 'It works' in result['data']['finding']['exploit']
        assert 'evidence' in result['data']['finding']
        assert 'evidence1' in result['data']['finding']['evidence']
        assert 'comments' in result['data']['finding']
        assert result['data']['finding']['comments'][0]['content'] == 'This is a comenting test'
        assert 'historicState' in result['data']['finding']
        assert 'title' in result['data']['finding']
        assert 'scenario' in result['data']['finding']
        assert 'actor' in result['data']['finding']
        assert 'description' in result['data']['finding']
        assert 'requirements' in result['data']['finding']
        assert 'attackVectorDesc' in result['data']['finding']
        assert 'threat' in result['data']['finding']
        assert 'recommendation' in result['data']['finding']
        assert 'affectedSystems' in result['data']['finding']
        assert 'compromisedAttributes' in result['data']['finding']
        assert 'compromisedRecords' in result['data']['finding']
        assert 'cweUrl' in result['data']['finding']
        assert 'btsUrl' in result['data']['finding']
        assert 'risk' in result['data']['finding']
        assert 'remediated' in result['data']['finding']
        assert 'type' in result['data']['finding']
        assert 'age' in result['data']['finding']
        assert 'isExploitable' in result['data']['finding']
        assert 'severityScore' in result['data']['finding']
        assert 'reportDate' in result['data']['finding']
        assert 'analyst' in result['data']['finding']
        assert 'historicTreatment' in result['data']['finding']
        assert 'currentState' in result['data']['finding']
        assert 'newRemediated' in result['data']['finding']
        assert 'verified' in result['data']['finding']
        assert 'observations' in result['data']['finding']
        assert result['data']['finding']['state'] == 'open'
        assert 'lastVulnerability' in result['data']['finding']
        assert 'historicState' in result['data']['finding']
        assert 'vulnerabilities' in result['data']['finding']
        assert result['data']['finding']['vulnerabilities'][0]['specific'] == 'phone'

    @pytest.mark.changes_db
    async def test_remove_evidence(self):
        """Check for removeEvidence mutation."""
        query = '''
            mutation RemoveEvidenceMutation($evidenceId: EvidenceType!, $findingId: String!) {
                removeEvidence(evidenceId: $evidenceId, findingId: $findingId) {
                success
                }
            }
        '''
        variables = {
            'evidenceId': 'EVIDENCE2',
            'findingId': '457497316'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeEvidence']

    @pytest.mark.changes_db
    async def test_update_evidence(self):
        """Check for updateEvidence mutation."""
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
        filename = os.path.join(filename, '../mock/test-anim.gif')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
            variables = {
                'evidenceId': 'ANIMATION',
                'findingId': '422286126',
                'file': uploaded_file
            }
            data = {'query': query, 'variables': variables}
            result = await self._get_result(data)
        if 'errors' not in result:
            assert 'errors' not in result
            assert 'success' in result['data']['updateEvidence']
            assert result['data']['updateEvidence']['success']
        else:
            pytest.skip("Expected error")

    @pytest.mark.changes_db
    async def test_update_evidence_description(self):
        """Check for updateEvidenceDescription mutation."""
        query = '''
            mutation {
                updateEvidenceDescription(
                description: "this is a test description",
                findingId: "422286126",
                evidenceId: EVIDENCE2) {
                success
                }
            }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidenceDescription']
        assert result['data']['updateEvidenceDescription']

    @pytest.mark.changes_db
    async def test_update_severity(self):
        """Check for updateSeverity mutation."""
        query = '''
                mutation {
                  updateSeverity (
                    findingId: "422286126",
                    data: {
            attackComplexity: 0.77, attackVector: 0.62,
            availabilityImpact: "0", availabilityRequirement: "1",
            confidentialityImpact: "0", confidentialityRequirement: "1",
            cvssVersion: "3.1", exploitability: 0.91, id: "422286126",
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
                    }
                  ) {
                    success
                    finding {
                      cvssVersion
                      severity
                    }
                  }
                }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateSeverity']
        assert result['data']['updateSeverity']['success']

    @pytest.mark.changes_db
    async def test_add_finding_comment_parent_zero(self):
        """Check for addFindingComment mutation."""
        query = '''
          mutation {
            addFindingComment(
              content: "This is a comenting test",
              findingId: "422286126",
              type: COMMENT,
              parent: "0"
            ) {
              success
              commentId
            }
          }
          '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addFindingComment']
        assert result['data']['addFindingComment']['success']

    @pytest.mark.changes_db
    async def test_add_finding_comment_parent_non_zero(self):
        """Check for addFindingComment mutation."""
        query = '''
          mutation {
            addFindingComment(
              content: "This is a comenting test",
              findingId: "422286126",
              type: COMMENT,
              parent: "1566336916294"
            ) {
              success
              commentId
            }
          }
          '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addFindingComment']
        assert result['data']['addFindingComment']['success']

    @pytest.mark.changes_db
    async def test_update_description(self):
        """Check for updateDescription mutation."""
        query = '''
            mutation UpdateFindingDescription(
                $actor: String!,
                $affectedSystems: String!,
                $attackVectorDesc: String!,
                $compromisedAttributes: String,
                $compromisedRecords: Int!,
                $cweUrl: String!,
                $description: String!,
                $findingId: String!,
                $recommendation: String!,
                $requirements: String!,
                $scenario: String!,
                $threat: String!,
                $title: String!,
                $type: String
            ){
                updateDescription(
                actor: $actor,
                affectedSystems: $affectedSystems,
                attackVectorDesc: $attackVectorDesc,
                cwe: $cweUrl,
                description: $description,
                findingId: $findingId,
                records: $compromisedAttributes,
                recommendation: $recommendation,
                recordsNumber: $compromisedRecords,
                requirements: $requirements,
                scenario: $scenario,
                threat: $threat,
                title: $title,
                findingType: $type
                ) {
                success
                }
            }
        '''
        variables = {
            'actor': 'ANYONE_INTERNET',
            'affectedSystems': 'Server bWAPP',
            'attackVectorDesc': 'This is an updated attack vector',
            'compromisedAttributes': 'Clave plana',
            'compromisedRecords': 12,
            'cweUrl': '200',
            'description': 'I just have updated the description',
            'findingId': '422286126',
            'recommendation': 'Updated recommendation',
            'requirements': 'REQ.0132. Passwords (phrase type) must be at least 3 words long.',
            'scenario': 'UNAUTHORIZED_USER_EXTRANET',
            'threat': 'Updated threat',
            'title': 'FIN.S.0051. Weak passwords reversed',
            'type': 'SECURITY'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateDescription']
        assert result['data']['updateDescription']['success']

    @pytest.mark.changes_db
    async def test_update_client_description(self):
        """Check for updateClientDescription mutation."""
        query = '''
            mutation {
                updateClientDescription (
                btsUrl: "",
                findingId: "463558592",
                treatment: ACCEPTED,
                justification: "This is a treatment justification test",
                acceptanceDate: "-"
                ) {
                success
                finding {
                    btsUrl
                    historicTreatment
                }
                }
            }
        '''
        data = {'query': query}
        result = await self._get_result(data, user='integratesuser@gmail.com')
        assert 'errors' not in result
        assert 'success' in result['data']['updateClientDescription']
        assert result['data']['updateClientDescription']['success']

    @pytest.mark.changes_db
    async def test_reject_draft(self):
        """Check for rejectDraft mutation."""
        query = '''
            mutation {
                rejectDraft(findingId: "836530833") {
                    success
                }
            }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['rejectDraft']
        assert result['data']['rejectDraft']

    @pytest.mark.changes_db
    async def test_delete_finding(self):
        """Check for deleteFinding mutation."""
        query = '''
          mutation {
            deleteFinding(findingId: "560175507", justification: NOT_REQUIRED) {
              success
            }
          }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['deleteFinding']
        assert result['data']['deleteFinding']['success']
        with pytest.raises(FindingNotFound):
            assert get_finding('560175507')

    @pytest.mark.changes_db
    async def test_approve_draft(self):
        """Check for approveDraft mutation."""
        query = '''
          mutation {
            approveDraft(draftId: "836530833") {
              success
            }
          }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'CANT_APPROVE_FINDING_WITHOUT_VULNS'

    @pytest.mark.changes_db
    async def test_create_draft(self):
        """Check for createDraft mutation."""
        query = '''
            mutation CreateDraftMutation(
                $cwe: String,
                $description: String,
                $projectName: String!,
                $recommendation: String,
                $requirements: String,
                $risk: String,
                $threat: String,
                $title: String!,
                $type: FindingType
                ) {
                createDraft(
                cwe: $cwe,
                description: $description,
                projectName: $projectName,
                recommendation: $recommendation,
                requirements: $requirements,
                risk: $risk,
                threat: $threat,
                title: $title,
                type: $type
                ) {
                success
                }
            }
        '''
        variables = {
            'cwe': '200',
            'description': 'This is pytest created draft',
            'projectName': 'UNITTESTING',
            'recommendation': 'Solve this finding',
            'requirements': 'REQ.0001. Apply filters',
            'risk': 'Losing money',
            'threat': 'Attacker',
            'title': 'FIN.S.0001. Very serious vulnerability',
            'type': 'SECURITY'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['createDraft']
        assert result['data']['createDraft']['success']

    @pytest.mark.changes_db
    async def test_submit_draft(self):
        """Check for submitDraft mutation."""
        query = '''
          mutation {
            submitDraft(findingId: "475041535") {
              success
            }
          }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' in result
        expected_error = 'Exception - This draft has missing fields: vulnerabilities'
        assert result['errors'][0]['message'] == expected_error

    @pytest.mark.changes_db
    async def test_handle_acceptation(self):
        """Check for handleAcceptation mutation."""
        query = '''
            mutation HandleAcceptationMutation(
                $findingId: String!,
                $observations: String!,
                $projectName: String!,
                $response: String!
                ) {
                handleAcceptation(
                findingId: $findingId,
                observations: $observations,
                projectName: $projectName,
                response: $response
                ) {
                success
                }
            }
        '''
        variables = {
            'findingId': '475041513',
            'observations': 'Test observations',
            'projectName': 'oneshottest',
            'response': 'IN PROGRESS'
        }
        data = {'query': query, 'variables': variables}
        result = await self._get_result(data, user='continuoushacking@gmail.com')
        assert 'errors' not in result
        assert 'success' in result['data']['handleAcceptation']
        assert result['data']['handleAcceptation']['success']

    @pytest.mark.changes_db
    async def test_filter_deleted_findings(self):
        """Check if vuln of deleted vulns are filter out."""
        query = '''
          query {
            project(projectName: "unittesting"){
              openVulnerabilities
            }
          }
        '''
        mutation = '''
          mutation {
            deleteFinding(findingId: "988493279", justification: NOT_REQUIRED) {
              success
            }
          }
        '''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        open_vulns = result['data']['project']['openVulnerabilities']

        data = {'query': mutation}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['deleteFinding']
        assert result['data']['deleteFinding']['success']

        data = {'query': query}
        result = await self._get_result(data)
        assert result['data']['project']['openVulnerabilities'] < open_vulns
