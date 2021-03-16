# Standard libraries
import os
import pytest

# Third party libraries
from starlette.datastructures import (
    UploadFile,
)

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence_description')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    draft: str = '475041513'
    description: str = 'this is a test description'
    evidence: str = 'EVIDENCE2'
    query = f'''
        mutation {{
                updateEvidenceDescription(
                description: "{description}",
                findingId: "{draft}",
                evidenceId: {evidence}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']
