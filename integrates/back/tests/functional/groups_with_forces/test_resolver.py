from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
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
    group_forces: str = "group2"
    group_not_forces: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert group_forces in result["data"]["groupsWithForces"]
    assert group_not_forces not in result["data"]["groupsWithForces"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("groups_with_forces")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_group_with_forces_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
