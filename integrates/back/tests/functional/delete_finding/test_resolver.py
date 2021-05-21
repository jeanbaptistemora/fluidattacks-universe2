# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("delete_finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_delete_finding(populate: bool, email: str):
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, str] = await query(
        user=email,
        finding=finding_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["deleteFinding"]
    assert result["data"]["deleteFinding"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("delete_finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_delete_finding_fail(populate: bool, email: str):
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, str] = await query(
        user=email,
        finding=finding_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
