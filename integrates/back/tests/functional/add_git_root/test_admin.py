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
@pytest.mark.resolver_test_group('add_git_root')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    group: str = 'group1'
    query = f'''
      mutation {{
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "{group}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/test1"
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
    assert result['data']['addGitRoot']['success']
