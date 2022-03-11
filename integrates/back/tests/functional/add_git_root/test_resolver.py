from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
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
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

    loaders = get_new_context()
    root_id = result["data"]["addGitRoot"]["rootId"]
    root = await loaders.root.load((group_name, root_id))
    assert root.cloning.status.value == "FAILED"
    assert root.cloning.reason == "Credentials does not work"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_git_root_fail_1(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
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
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_add_git_root_fail_2(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
