from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("edit_stakeholder_organization")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
    ],
)
async def test_edit_stakeholder_organization(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "CUSTOMER"
    user_phone: str = "12345678"
    result: Dict[str, Any] = await query(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
        phone=user_phone,
    )
    assert "errors" not in result
    assert result["data"]["editStakeholderOrganization"]["success"]
    assert (
        result["data"]["editStakeholderOrganization"]["modifiedStakeholder"][
            "email"
        ]
        == email
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("edit_stakeholder_organization")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_edit_stakeholder_organization_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "CUSTOMER"
    user_phone: str = "12345678"
    result: Dict[str, Any] = await query(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
        phone=user_phone,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
