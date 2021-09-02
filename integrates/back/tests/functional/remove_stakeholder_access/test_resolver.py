from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_remove_stakeholder_access(populate: bool, email: str) -> None:
    assert populate
    stakeholder_email: str = "admin@gmail.com"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeStakeholderAccess"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_remove_stakeholder_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    stakeholder_email: str = "hacker@gmail.com"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
