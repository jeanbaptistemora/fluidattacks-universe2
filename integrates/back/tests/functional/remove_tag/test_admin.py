# Standard libraries
import pytest
from typing import (
    List,
)

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_tag')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    tag: str = 'test1'
    group: str = 'group1'
    query = f'''
        mutation {{
            removeTag (
            tag: "{tag}",
            projectName: "{group}",
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
    assert 'success' in result['data']['removeTag']
    assert result['data']['removeTag']['success']

    context = get_new_context()
    query = f'''
        query {{
            project(projectName: "{group}"){{
                tags
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
    assert result['data']['project']['tags'] == ['test2']
