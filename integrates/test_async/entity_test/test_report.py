import os
from datetime import datetime, timedelta
import pytest
from PyPDF4 import PdfFileWriter

from backend.api import apply_context_attrs
from ariadne import graphql_sync, graphql
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session
from __init__ import (
    STARTDIR
)


pytestmark = pytest.mark.asyncio

async def test_finding_report():
    query_pdf = '''
        query test {
            report(
                projectName: "oneshottest",
                reportType: PDF,
                lang: EN) {
                url
            }
        }
    '''
    query_xls = '''
        query test {
            report(
                projectName: "oneshottest",
                reportType: XLS) {
                url
            }
        }
    '''
    query_data = '''
        query test {
            report(
                projectName: "oneshottest",
                reportType: DATA) {
                url
            }
        }
    '''
    data_pdf = {'query': query_pdf}
    data_xls = {'query': query_xls}
    data_data = {'query': query_data}
    request = await create_dummy_session('integratesmanager@gmail.com')
    request = apply_context_attrs(request)
    _, result_pdf = await graphql(SCHEMA, data_pdf, context_value=request)
    _, result_xls = await graphql(SCHEMA, data_xls, context_value=request)
    _, result_data = await graphql(SCHEMA, data_data, context_value=request)
    assert all('url' in result['data']['report'] and
        result['data']['report']['url']
        for result in [result_xls, result_data, result_pdf])

async def test_all_vulns_report():
    query_all_vulns = '''
        query test {
            report(reportType: ALL_VULNS, projectName: "oneshottest") {
                url
            }
        }
    '''
    data_all_vulns = {'query': query_all_vulns}
    request = await create_dummy_session('integratesmanager@gmail.com')
    _, result_all_vulns = await graphql(
        SCHEMA,
        data_all_vulns,
        context_value=request
    )
    assert ('url' in result_all_vulns['data']['report']
        and result_all_vulns['data']['report']['url'])

async def test_all_users_report():
    query_all_users = '''
        query test {
            report(reportType: ALL_USERS) {
                url
            }
        }
    '''
    data_all_users = {'query': query_all_users}
    request = await create_dummy_session('integratesmanager@gmail.com')
    _, result_all_users = await graphql(
        SCHEMA,
        data_all_users,
        context_value=request
    )
    assert ('url' in result_all_users['data']['report']
        and result_all_users['data']['report']['url'])

def test_pdf_paths():
    # secure_pdf.py paths
    base = (
        f'{STARTDIR}/integrates/back/packages/'
        'integrates-back/backend/reports'
    )
    secure_pdf_paths = [
        base,
        f'{base}/results/results_pdf/',
        f'{base}/resources/themes/watermark_integrates_en.pdf',
        f'{base}/resources/themes/overlay_footer.pdf',
    ]

    for path in secure_pdf_paths:
        assert os.path.exists(path), f'path: {path} is not valid'

    # pdf.py paths
    path = (
        f'{STARTDIR}/integrates/back/packages/'
        'integrates-back/backend/reports'
    )
    pdf_paths = [
        path,
        f'{path}/resources/fonts',
        f'{path}/resources/themes',
        f'{path}/results/results_pdf/',
        f'{path}/templates/pdf/executive.adoc',
        f'{path}/templates/pdf/tech.adoc',
        f'{path}/tpls/',
    ]

    for path in pdf_paths:
        assert os.path.exists(path), f'path: {path} is not valid'
