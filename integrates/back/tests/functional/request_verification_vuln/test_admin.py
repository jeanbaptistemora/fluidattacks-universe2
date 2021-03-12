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
@pytest.mark.resolver_test_group('request_verification_vuln')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    finding: str = '475041513'
    vulnerability: str = 'be09edb7-cd5c-47ed-bee4-97c645acdce8'
    context = get_new_context()
    query = f'''
        mutation {{
            requestVerificationVuln(
                findingId: "{finding}",
                justification: "this is a comenting test of a request verification in vulns",
                vulnerabilities:
                    ["{vulnerability}"]
            ) {{
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
    assert result['data']['requestVerificationVuln']['success']
