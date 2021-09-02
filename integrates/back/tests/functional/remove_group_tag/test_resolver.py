from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group_tag")
@pytest.mark.parametrize(
    ("email", "tag_name"),
    (
        ("admin@gmail.com", "test1"),
        ("customer@gmail.com", "test2"),
        ("customeradmin@gmail.com", "test3"),
        ("executive@gmail.com", "test4"),
        ("system_owner@gmail.com", "test5"),
    ),
)
async def test_remove_group_tag(
    populate: bool, email: str, tag_name: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeGroupTag"]
    assert result["data"]["removeGroupTag"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group_tag")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_remove_group_tag_fail(populate: bool, email: str) -> None:
    assert populate
    tag_name: str = "test2"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
