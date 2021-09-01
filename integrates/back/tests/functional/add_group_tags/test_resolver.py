from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_tags")
@pytest.mark.parametrize(
    ("email", "tag_list"),
    (
        ("admin@gmail.com", ["testing1"]),
        ("customer@gmail.com", ["testing2"]),
        ("customeradmin@gmail.com", ["testing3"]),
        ("executive@gmail.com", ["testing4"]),
        ("group_manager@gmail.com", ["testing5"]),
    ),
)
async def test_add_group_tags(
    populate: bool, email: str, tag_list: List[str]
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        tags=tag_list,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupTags"]
    assert result["data"]["addGroupTags"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_group_tags_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    tag_list: List[str] = ["testing"]
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        tags=tag_list,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
