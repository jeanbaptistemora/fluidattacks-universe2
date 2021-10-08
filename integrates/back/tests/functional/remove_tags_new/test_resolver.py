from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_remove_tags(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln=vuln_uuid
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTags"]
    assert result["data"]["removeTags"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_remove_tags_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln=vuln_uuid
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
