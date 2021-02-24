# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from test_functional.analyst.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_report():
    context = get_new_context()
    group_name = 'unittesting'
    query = f'''
        query {{
            report(
                projectName: "{group_name}",
                reportType: PDF,
                lang: EN
            ) {{
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'url' in result['data']['report']
    assert result['data']['report']['url'] == 'The report will be sent to integratesanalyst@fluidattacks.com shortly'

    query = f'''
        query {{
            report(
                projectName: "{group_name}",
                reportType: XLS
            ) {{
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'url' in result['data']['report']
    assert result['data']['report']['url'] == 'The report will be sent to integratesanalyst@fluidattacks.com shortly'

    query = f'''
        query {{
            report(
                projectName: "{group_name}",
                reportType: DATA) {{
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'url' in result['data']['report']
    assert result['data']['report']['url'] == 'The report will be sent to integratesanalyst@fluidattacks.com shortly'
