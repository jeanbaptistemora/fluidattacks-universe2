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
@pytest.mark.resolver_test_group("add_group_tags")
@pytest.mark.parametrize(
    ("email", "tag_to_add"),
    (
        ("admin@gmail.com", "testing1"),
        ("user@gmail.com", "testing2"),
        ("user_manager@gmail.com", "testing3"),
        ("vulnerability_manager@gmail.com", "testing4"),
        ("executive@gmail.com", "testing5"),
        ("customer_manager@fluidattacks.com", "testing6"),
    ),
)
async def test_add_group_tags(
    populate: bool, email: str, tag_to_add: str
) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    if group.tags:
        assert tag_to_add not in group.tags

    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        tags=[tag_to_add],
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupTags"]
    assert result["data"]["addGroupTags"]["success"]

    loaders.group_typed.clear(group_name)
    group = await loaders.group_typed.load(group_name)
    if group.tags:
        assert tag_to_add in group.tags
    else:
        assert group.tags is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_group_tags_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    tag_list: list[str] = ["testing"]
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        tags=tag_list,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
