# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tag")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_tag(populate: bool, email: str):
    assert populate
    tag_name: str = "test1"
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTag"]
    assert result["data"]["removeTag"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tag")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_remove_tag_fail(populate: bool, email: str):
    assert populate
    tag_name: str = "test2"
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
