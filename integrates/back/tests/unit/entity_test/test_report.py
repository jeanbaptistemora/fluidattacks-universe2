import os
import pytest

from ariadne import graphql

from back.tests.unit.utils import create_dummy_session
from backend.api import apply_context_attrs
from backend.api.schema import SCHEMA
from __init__ import STARTDIR


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

def test_pdf_paths():
    # secure_pdf.py paths
    base = f'{STARTDIR}/integrates/back/packages/modules/reports'
    secure_pdf_paths = [
        base,
        f'{base}/results/results_pdf/',
        f'{base}/resources/themes/watermark_integrates_en.pdf',
        f'{base}/resources/themes/overlay_footer.pdf',
    ]

    for path in secure_pdf_paths:
        assert os.path.exists(path), f'path: {path} is not valid'

    # pdf.py paths
    path = f'{STARTDIR}/integrates/back/packages/modules/reports'
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
