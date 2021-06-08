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
@pytest.mark.resolver_test_group("add_tags")
@pytest.mark.parametrize(
    ("email", "tag_list"),
    (
        ("admin@gmail.com", ["testing1"]),
        ("customer@gmail.com", ["testing2"]),
    ),
)
async def test_add_tags(
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
async def test_add_tags_fail(populate: bool, email: str) -> None:
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
