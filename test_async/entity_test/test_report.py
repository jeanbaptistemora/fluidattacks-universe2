import os
import pytest
from PyPDF4 import PdfFileWriter

from ariadne import graphql_sync, graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class ReportTests(TestCase):

    async def test_request_report(self):
        query = '''
            mutation {
                requestProjectReport(
                    projectName: "oneshottest",
                    reportType: PDF,
                    lang: EN) {
                    success
                }
            }
        '''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesmanager@gmail.com'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['requestProjectReport'] and \
            result['data']['requestProjectReport']['success']
