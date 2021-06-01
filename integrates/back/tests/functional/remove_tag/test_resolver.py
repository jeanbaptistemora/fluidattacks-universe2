from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tag")
@pytest.mark.parametrize(
    ("email", "tag_name"),
    (
        ("admin@gmail.com", "test1"),
        ("customer@gmail.com", "test2"),
    ),
)
async def test_remove_tag(populate: bool, email: str, tag_name: str) -> None:
    assert populate
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
async def test_remove_tag_fail(populate: bool, email: str) -> None:
    assert populate
    tag_name: str = "test2"
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
