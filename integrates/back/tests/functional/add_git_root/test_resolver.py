from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_git_root(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
    ],
)
async def test_add_git_root_fail_1(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Active root with the same Nickname already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_add_git_root_fail_2(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
