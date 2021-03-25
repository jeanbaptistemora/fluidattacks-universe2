# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_file')
async def test_admin(populate: bool):
    assert populate
    file_name: str = 'test.zip'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group='group-1',
        f_name=file_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_file')
async def test_analyst(populate: bool):
    assert populate
    file_name: str = 'test.zip'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group='group-1',
        f_name=file_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']
