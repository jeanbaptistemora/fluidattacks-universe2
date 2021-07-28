from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_update_organization_stakeholder(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "CUSTOMER"
    user_phone: str = "12345678"
    result: Dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
        phone=user_phone,
    )
    assert "errors" not in result
    assert result["data"]["updateOrganizationStakeholder"]["success"]
    assert (
        result["data"]["updateOrganizationStakeholder"]["modifiedStakeholder"][
            "email"
        ]
        == email
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_update_organization_stakeholder_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "CUSTOMER"
    user_phone: str = "12345678"
    result: Dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
        phone=user_phone,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
