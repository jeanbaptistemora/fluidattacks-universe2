# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('resources')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group='group-1',
    )
    assert result['data']['resources']['projectName'] == 'group-1'
    assert 'test.zip' in result['data']['resources']['files']
    assert 'shell.exe' in result['data']['resources']['files']
    assert 'shell2.exe' in result['data']['resources']['files']
    assert 'asdasd.py' in result['data']['resources']['files']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('resources')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group='group-1',
    )
    assert result['data']['resources']['projectName'] == 'group-1'
    assert 'test.zip' in result['data']['resources']['files']
    assert 'shell.exe' in result['data']['resources']['files']
    assert 'shell2.exe' in result['data']['resources']['files']
    assert 'asdasd.py' in result['data']['resources']['files']
