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
@pytest.mark.resolver_test_group("add_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_tags(populate: bool, email: str):
    assert populate
    group_name: str = "group1"
    tag_list: List[str] = ["testing"]
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
        tags=tag_list,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addTags"]
    assert result["data"]["addTags"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_add_tags_fail(populate: bool, email: str):
    assert populate
    group_name: str = "group1"
    tag_list: List[str] = ["testing"]
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
        tags=tag_list,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
