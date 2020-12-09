import os
from datetime import datetime, timedelta
import pytest
from PyPDF4 import PdfFileWriter

from ariadne import graphql_sync, graphql
from jose import jwt
from backend import util
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session


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
    request.loaders = {
        'group_findings': GroupFindingsLoader(),
    }
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
