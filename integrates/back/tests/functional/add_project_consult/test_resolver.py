# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_project_consult')
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group=group_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_project_consult')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group=group_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['addProjectConsult']
    assert result['data']['addProjectConsult']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_project_consult')
async def test_closer(populate: bool):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        group=group_name,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
