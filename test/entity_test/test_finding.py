import os
from collections import OrderedDict

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene.test import Client
from jose import jwt

from backend.api.schema import SCHEMA
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.domain.finding import get_finding
from backend.exceptions import FindingNotFound, NotVerificationRequested


class FindingTests(TestCase):

    def _get_result(self, query, testing_client, request_loaders):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.loaders = request_loaders
        if testing_client:

            return testing_client.execute(query, context=request)

        return SCHEMA.execute(query, context=request)

    def test_delete_finding(self):
        query = '''
          mutation {
            deleteFinding(findingId: "560175507", justification: NOT_REQUIRED) {
              success
            }
          }
        '''
        testing_client = Client(SCHEMA)
        request_loaders = {'finding': FindingLoader()}
        result = self._get_result(query, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['deleteFinding']['success']
        with pytest.raises(FindingNotFound):
          assert get_finding('560175507')

    def test_get_finding(self):
        """ Check for finding """
        query = '''{
          finding(identifier: "422286126"){
            id
            vulnerabilities {
                findingId
                id
                historicState
                specific
                vulnType
                where
            }
          }
        }'''
        request_loaders = {
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        result = self._get_result(query, False, request_loaders)
        assert not result.errors
        assert result.data.get('finding')['id'] == '422286126'
        test_data = OrderedDict([
            ('findingId', '422286126'),
            ('id', '80d6a69f-a376-46be-98cd-2fdedcffdcc0'),
            ('historicState',
             [{'date': '2018-09-28 10:32:58', 'state': 'open', 'analyst':'test@unittesting.com'},
              {'date': '2019-01-08 16:01:26', 'state': 'open', 'analyst':'test@unittesting.com'}]),
            ('specific', 'phone'),
            ('vulnType', 'inputs'),
            ('where', 'https://example.com')])
        assert test_data in result.data.get('finding')['vulnerabilities']

    def test_update_evidence(self):
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
        testing_client = Client(SCHEMA)
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-anim.gif')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        variables = {
            'evidenceId': 'ANIMATION',
            'file': uploaded_file,
            'findingId': '422286126'
        }
        result = testing_client.execute(
            query, context=request, variables=variables)
        assert 'errors' not in result
        assert result['data']['updateEvidence']['success']

    def test_update_evidence_description(self):
        query = '''
                mutation {
                  updateDescription: updateEvidenceDescription (
                    description: "this is a test description",
                    findingId: "422286126",
                    evidenceId: EVIDENCE2) {
                  success
                  }
                }
        '''
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client, None)
        assert 'errors' not in result
        assert result['data']['updateDescription']['success']

    def test_update_severity(self):
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
        testing_client = Client(SCHEMA)
        request_loaders = {'finding': FindingLoader()}
        result = self._get_result(query, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['updateSeverity']['success']

    def test_add_finding_comment(self):
        query = '''
          mutation {
            addFindingComment(
              content: "This is a comenting test",
              findingId: "422286126",
              type: "comment",
              parent: "0"
            ) {
              success
              commentId
            }
          }
          '''
        testing_client = Client(SCHEMA)
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.session['first_name'] = 'unit'
        request.session['last_name'] = 'test'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest@fluidattacks.com',
                'user_role': 'admin',
                'company': 'unittest',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['addFindingComment']['success']

    def test_update_treatment_accepted(self):
        query = '''
                mutation {
                  updateClientDescription (
                    btsUrl: "",
                    findingId: "463558592",
                    treatment: "ACCEPTED",
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
        testing_client = Client(SCHEMA)
        request_loaders = {
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()}
        result = self._get_result(query, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['updateClientDescription']['success']

    def test_update_treatment_new(self):
        query = '''
                mutation {
                  updateClientDescription (
                    btsUrl: "",
                    findingId: "436992569",
                    treatment: "NEW",
                    justification: ""
                  ) {
                    success
                    finding {
                      btsUrl
                      historicTreatment
                    }
                  }
                }
        '''
        testing_client = Client(SCHEMA)
        request_loaders = {
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()}
        result = self._get_result(query, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['updateClientDescription']['success']

    def test_update_external_bts(self):
        query_bts = '''
                mutation {
                  updateClientDescription (
                    btsUrl: "new test btsUrl",
                    findingId: "436992569",
                    treatment: "NEW",
                    justification: ""
                  ) {
                    success
                    finding {
                      btsUrl
                      historicTreatment
                    }
                  }
                }
        '''
        testing_client = Client(SCHEMA)
        request_loaders = {
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()}
        result = self._get_result(query_bts, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['updateClientDescription']['success']
        query_bts_empty = '''
                mutation {
                  updateClientDescription (
                    btsUrl: "",
                    findingId: "436992569",
                    treatment: "NEW",
                    justification: ""
                  ) {
                    success
                    finding {
                      btsUrl
                      historicTreatment
                    }
                  }
                }
        '''
        testing_client = Client(SCHEMA)
        request_loaders = {
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()}
        result = self._get_result(query_bts_empty, testing_client, request_loaders)
        assert 'errors' not in result
        assert result['data']['updateClientDescription']['success']

    def test_verify_finding(self):
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
        testing_client = Client(SCHEMA)
        request_loaders = {'finding': FindingLoader()}
        result = self._get_result(query, testing_client, request_loaders)
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(NotVerificationRequested())
