import os
from datetime import datetime, timedelta
import pytest
from PyPDF4 import PdfFileWriter

from ariadne import graphql_sync, graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.project import ProjectLoader
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class ReportTests(TestCase):

    def create_dummy_session(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesmanager@gmail.com'
        request.session['company'] = 'unittest'
        payload = {
            'user_email': 'integratesmanager@gmail.com',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': util.calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        return request

    @pytest.mark.changes_db
    async def test_request_report(self):
        query_pdf = '''
            mutation {
                requestProjectReport(
                    projectName: "oneshottest",
                    reportType: PDF,
                    lang: EN) {
                    success
                }
            }
        '''
        query_xls = '''
            mutation {
                requestProjectReport(
                    projectName: "oneshottest",
                    reportType: XLS) {
                    success
                }
            }
        '''
        data_pdf = {'query': query_pdf}
        data_xls = {'query': query_xls}
        request = self.create_dummy_session()
        request.loaders = {
            'project': ProjectLoader(),
        }
        _, result_pdf = await graphql(SCHEMA, data_pdf, context_value=request)
        _, result_xls = await graphql(SCHEMA, data_xls, context_value=request)
        assert any('errors' not in result for result in [result_pdf, result_xls])
        assert all('success' in result['data']['requestProjectReport'] and
            result['data']['requestProjectReport']['success']
            for result in [result_pdf, result_xls])
