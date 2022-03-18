from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group_tag")
@pytest.mark.parametrize(
    ("email", "tag_name"),
    (
        ("admin@gmail.com", "test1"),
        ("user@gmail.com", "test2"),
        ("user_manager@gmail.com", "test3"),
        ("executive@gmail.com", "test4"),
        ("customer_manager@fluidattacks.com", "test5"),
        ("vulnerability_manager@gmail.com", "test6"),
    ),
)
async def test_remove_group_tag(
    populate: bool, email: str, tag_name: str
) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert tag_name in group.tags

    result: dict[str, Any] = await get_result(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeGroupTag"]
    assert result["data"]["removeGroupTag"]["success"]

    loaders.group_typed.clear(group_name)
    group = await loaders.group_typed.load(group_name)
    if group.tags:
        assert tag_name not in group.tags
    else:
        assert group.tags is None


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
    result: dict[str, Any] = await get_result(
        user=email, group=group_name, tag=tag_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
