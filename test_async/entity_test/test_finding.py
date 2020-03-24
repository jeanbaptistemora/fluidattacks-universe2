import json
import os

from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied


class FindingTests(TestCase):

    def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'user_role': 'admin',
                'company': 'fluid',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        return result

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
