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
@pytest.mark.resolver_test_group('update_event_evidence')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'admin@gmail.com'
    event: str = '418900971'
    query = '''
        mutation updateEventEvidence(
            $eventId: String!, $evidenceType: EventEvidenceType!, $file: Upload!
            ) {
            updateEventEvidence(eventId: $eventId,
                                evidenceType: $evidenceType,
                                file: $file) {
                success
            }
        }
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    filename = f'{path}/test-anim.gif'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'image/gif')
        variables = {
            'eventId': event,
            'evidenceType': 'IMAGE',
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}

        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=context,
        )
    assert result['data']['updateEventEvidence']['success']
