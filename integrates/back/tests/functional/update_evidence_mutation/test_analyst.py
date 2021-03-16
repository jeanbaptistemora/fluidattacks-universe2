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
@pytest.mark.resolver_test_group('update_evidence_mutation')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    draft: str = '475041513'
    query = '''
        mutation UpdateEvidenceMutation(
            $evidenceId: EvidenceType!, $file: Upload!, $findingId: String!
        ) {
            updateEvidence(
                evidenceId: $evidenceId, file: $file, findingId: $findingId
            ) {
                success
            }
        }
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    filename = f'{path}/test-anim.gif'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'image/gif')
        variables = {
            'evidenceId': 'ANIMATION',
            'findingId': draft,
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=context,
        )
        assert 'errors' not in result
        assert 'success' in result['data']['updateEvidence']
        assert result['data']['updateEvidence']['success']
