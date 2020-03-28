from collections import OrderedDict
import json
import os
import pytest

from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from graphql import GraphQLError
from jose import jwt
from backend.api.schema import SCHEMA
from backend.domain.finding import get_finding
from backend.exceptions import FindingNotFound, NotVerificationRequested


class FindingTests(TestCase):

    def _get_result(self, data):
        """Get result."""
        request = RequestFactory().post('/',
                                        {'data': 'finding(identifier: "422286126")'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        return result

    def test_finding(self):
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
          }
        }'''
        data = {'query': query}
        result = self._get_result(data)
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

    def test_remove_evidence(self):
        """Check for removeEvidence mutation."""
        query = '''
            mutation RemoveEvidenceMutation($evidenceId: EvidenceType!, $findingId: String!) {
                removeEvidence(evidenceId: $evidenceId, findingId: $findingId) {
                success
                }
            }
        '''
        variables = {
            'evidenceId': 'EVIDENCE1',
            'findingId': '457497316'
        }
        data = {'query': query, 'variables': variables}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeEvidence']

    def test_update_evidence(self):
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
        filename = os.path.join(filename, '../../test/mock/test-anim.gif')
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']

    def test_update_evidence_description(self):
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidenceDescription']
        assert result['data']['updateEvidenceDescription']

    def test_verify_finding(self):
        """Check for verifyFinding mutation."""
        query = '''
          mutation {
            verifyFinding(
                findingId: "463461507",
                justification: "This is a commenting test, of the verifying of a request."
            ) {
              success
            }
          }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(NotVerificationRequested())

    def test_reject_draft(self):
        """Check for rejectDraft mutation."""
        query = '''
            mutation {
                rejectDraft(findingId: "836530833") {
                    success
                }
            }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['rejectDraft']
        assert result['data']['rejectDraft']

    def test_delete_finding(self):
        """Check for deleteFinding mutation."""
        query = '''
          mutation {
            deleteFinding(findingId: "560175507", justification: NOT_REQUIRED) {
              success
            }
          }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['deleteFinding']
        assert result['data']['deleteFinding']['success']
        with pytest.raises(FindingNotFound):
            assert get_finding('560175507')

    def test_approve_draft(self):
        """Check for approveDraft mutation."""
        query = '''
          mutation {
            approveDraft(draftId: "836530833") {
              success
            }
          }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'CANT_APPROVE_FINDING_WITHOUT_VULNS'

    def test_create_draft(self):
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['createDraft']
        assert result['data']['createDraft']['success']

    def test_submit_draft(self):
        """Check for submitDraft mutation."""
        query = '''
          mutation {
            submitDraft(findingId: "475041535") {
              success
            }
          }
        '''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' in result
        expected_error = 'Exception - This draft has missing fields: vulnerabilities'
        assert result['errors'][0]['message'] == expected_error
