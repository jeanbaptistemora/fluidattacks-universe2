# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_tags')
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group1'
    tag_list: List[str] = ['testing']
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group=group_name,
        tags=tag_list,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['addTags']
    assert result['data']['addTags']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_tags')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group1'
    tag_list: List[str] = ['testing']
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group=group_name,
        tags=tag_list,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_tags')
async def test_closer(populate: bool):
    assert populate
    group_name: str = 'group1'
    tag_list: List[str] = ['testing']
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        group=group_name,
        tags=tag_list,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
