from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
async def test_admin(populate: bool) -> None:
    assert populate
    org_name: str = "TESTORG"
    result: Dict[str, Any] = await get_result(
        user="admin@gmail.com", org=org_name
    )
    assert "errors" not in result
    assert result["data"]["addOrganization"]["success"]
    assert (
        result["data"]["addOrganization"]["organization"]["name"]
        == org_name.lower()
    )
    assert result["data"]["addOrganization"]["organization"]["id"].startswith(
        "ORG"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
async def test_analyst(populate: bool) -> None:
    assert populate
    org_name: str = "TESTORG"
    result: Dict[str, Any] = await get_result(
        user="hacker@gmail.com", org=org_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
