from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_stakeholder")
@pytest.mark.parametrize(
    ["granting_email", "modified_email", "modified_role"],
    [
        ["admin@gmail.com", "user@gmail.com", "VULNERABILITY_MANAGER"],
        ["user_manager@gmail.com", "user@gmail.com", "USER_MANAGER"],
        ["customer_manager@fluidattacks.com", "user@gmail.com", "USER"],
    ],
)
async def test_update_group_stakeholder(
    populate: bool,
    granting_email: str,
    modified_email: str,
    modified_role: str,
) -> None:
    assert populate
    group_name: str = "group1"
    stakeholder_responsibility: str = "Test"
    result: dict[str, Any] = await get_result(
        granting_email=granting_email,
        group=group_name,
        modified_email=modified_email,
        modified_role=modified_role,
        responsibility=stakeholder_responsibility,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupStakeholder"]
    assert result["data"]["updateGroupStakeholder"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_update_group_stakeholder_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    stakeholder_responsibility: str = "Test"
    stakeholder_role: str = "USER"
    result: dict[str, Any] = await get_result(
        granting_email=email,
        group=group_name,
        modified_email=email,
        modified_role=stakeholder_role,
        responsibility=stakeholder_responsibility,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
