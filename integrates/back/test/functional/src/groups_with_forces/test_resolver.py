from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("groups_with_forces")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_group_with_forces(populate: bool, email: str) -> None:
    assert populate
    group_names = [
        "group1",
        "group2",
        "group3",
    ]
    result: dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    for group_name in group_names:
        assert group_name in result["data"]["groupsWithForces"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("groups_with_forces")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_group_with_forces_fail(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
