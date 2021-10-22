from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
@pytest.mark.parametrize(
    ("description", "language"),
    (
        ("Description test", "EN"),
        ("Description test", "ES"),
    ),
)
async def test_update_group_info(
    populate: bool,
    description: str,
    email: str,
    language: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        description=description,
        language=language,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupInfo"]
    assert result["data"]["updateGroupInfo"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["customer@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
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
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        description=description,
        language=language,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
