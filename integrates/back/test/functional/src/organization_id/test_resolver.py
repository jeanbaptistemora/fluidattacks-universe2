from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_id")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
async def test_get_organization_id(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(user=email, org=org_name)
    assert "errors" not in result
    assert result["data"]["organizationId"]["id"] == org_id


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_id")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["vulnerability_manager@fluidattacks.com"],
    ],
)
async def test_get_organization_id_fail(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest2"
    result: Dict[str, Any] = await get_result(user=email, org=org_name)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Access denied or organization not found"
    )
