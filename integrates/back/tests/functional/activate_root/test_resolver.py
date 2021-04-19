# Standard
import pytest
from typing import Any, Dict

# Local
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('activate_root')
async def test_git_root(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        email='admin@gmail.com',
        group_name='group1',
        id='63298a73-9dff-46cf-b42d-9b2f01a56690'
    )
    assert 'errors' not in result
    assert result['data']['activateRoot']['success']
