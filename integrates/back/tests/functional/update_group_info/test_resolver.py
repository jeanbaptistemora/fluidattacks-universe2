from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupLanguage,
)
from db_model.groups.types import (
    Group,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ("email", "language"),
    (
        ("admin@gmail.com", "EN"),
        ("user_manager@gmail.com", "ES"),
        ("customer_manager@fluidattacks.com", "ES"),
    ),
)
async def test_update_group_info(
    populate: bool,
    email: str,
    language: str,
) -> None:
    assert populate
    group_name: str = "group1"
    description: str = f"Description test modified by {email}"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        description=description,
        language=language,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupInfo"]
    assert result["data"]["updateGroupInfo"]["success"]

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.description == description
    assert group.language == GroupLanguage[language]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
@pytest.mark.parametrize(
    ("description", "language"),
    (
        ("Description test", "EN"),
        ("Description test", "ES"),
    ),
)
async def test_update_group_info_fail(
    populate: bool,
    description: str,
    email: str,
    language: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        description=description,
        language=language,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
