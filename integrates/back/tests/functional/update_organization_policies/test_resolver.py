from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
    ],
)
async def test_update_organization_policies(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    result: Dict[str, Any] = await get_result(
        user=email,
        identifier=org_id,
        name=org_name,
    )
    assert "errors" not in result
    assert result["data"]["updateOrganizationPolicies"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_update_organization_policies_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    result: Dict[str, Any] = await get_result(
        user=email,
        identifier=org_id,
        name=org_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
