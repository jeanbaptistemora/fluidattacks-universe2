from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_remove_stakeholder_organization_access(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, stakeholder=email
    )
    assert "errors" not in result
    assert result["data"]["removeStakeholderOrganizationAccess"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_remove_stakeholder_organization_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, stakeholder=email
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
