# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)
from backend.exceptions import (
    UserNotInOrganization,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('finding')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin = 'test1@gmail.com'
    open_vuln = '6401bc87-8633-4a4a-8d8e-7dae0ca57e6a'
    closed_vuln = 'be09edb7-cd5c-47ed-bee4-97c645acdce8'
    finding_id = '475041513'
    query = f'''
        query {{
            finding(identifier: "{finding_id}"){{
                vulnerabilities{{
                    id
                    where
                }}
                openVulnerabilities
                closedVulnerabilities
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
    vuln_ids = [vuln['id'] for vuln in result['data']['finding']['vulnerabilities']]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result['data']['finding']['openVulnerabilities'] == 1
    assert result['data']['finding']['closedVulnerabilities'] == 1
