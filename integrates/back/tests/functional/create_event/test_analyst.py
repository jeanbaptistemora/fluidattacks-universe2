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
@pytest.mark.resolver_test_group('create_event')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    group: str = 'group1'
    query = f'''
        mutation {{
            createEvent(
                projectName: "{group}",
                actionAfterBlocking: TRAINING,
                actionBeforeBlocking: DOCUMENT_PROJECT,
                accessibility: ENVIRONMENT,
                context: CLIENT,
                detail: "analyst create new event",
                eventDate: "2020-02-01T00:00:00Z",
                eventType: INCORRECT_MISSING_SUPPLIES
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
    assert result['data']['createEvent']
