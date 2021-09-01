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
async def test_admin(populate: bool) -> None:
    assert populate
    org_name: str = "orgtest"
    result: Dict[str, Any] = await get_result(
        user="admin@gmail.com", org=org_name
    )
    assert "errors" not in result
    assert (
        result["data"]["organizationId"]["id"]
        == "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_id")
async def test_analyst(populate: bool) -> None:
    assert populate
    org_name: str = "orgtest"
    result: Dict[str, Any] = await get_result(
        user="hacker@gmail.com", org=org_name
    )
    assert "errors" not in result
    assert (
        result["data"]["organizationId"]["id"]
        == "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    )
