from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_group_stakeholder(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    stakeholder_responsibility: str = "Test"
    stakeholder_role: str = "ADMIN"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupStakeholder"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_update_group_stakeholder_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    stakeholder_responsibility: str = "Test"
    stakeholder_role: str = "ADMIN"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
