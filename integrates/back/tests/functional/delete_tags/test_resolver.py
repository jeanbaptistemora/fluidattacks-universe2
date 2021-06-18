from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("delete_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
    ],
)
async def test_delete_tags(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln=vuln_uuid
    )
    assert "errors" not in result
    assert "success" in result["data"]["deleteTags"]
    assert result["data"]["deleteTags"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("delete_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_delete_tags_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln=vuln_uuid
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
