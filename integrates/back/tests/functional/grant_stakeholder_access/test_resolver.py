from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_grant_stakeholder_access(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group2"
    stakeholder_email: str = "hacker@gmail.com"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "EXECUTIVE"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" not in result
    assert result["data"]["grantStakeholderAccess"]["success"]
    assert (
        result["data"]["grantStakeholderAccess"]["grantedStakeholder"]["email"]
        == stakeholder_email
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_grant_stakeholder_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group2"
    stakeholder_email: str = "hacker@gmail.com"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "EXECUTIVE"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
