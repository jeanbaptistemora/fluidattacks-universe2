# Standard libraries
import os
import pytest

# Third party libraries
from starlette.datastructures import UploadFile

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_vuln_file')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    group = 'group1'
    finding: str = '475041513'
    context = get_new_context()
    query = f'''
        mutation {{
            downloadVulnFile (findingId: "{finding}") {{
                url
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['downloadVulnFile']['success']
    assert 'url' in result['data']['downloadVulnFile']
    assert f'localhost:9000/fluidintegrates.reports/{group}-{finding}' \
        in result['data']['downloadVulnFile']['url']
