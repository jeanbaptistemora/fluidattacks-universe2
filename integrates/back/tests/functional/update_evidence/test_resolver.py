from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_update_evidence(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    result: Dict[str, Any] = await get_result(user=email, draft=draft_id)
    assert "errors" not in result
    assert "success" in result["data"]["updateEvidence"]
    assert result["data"]["updateEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_update_evidence_fail(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    result: Dict[str, Any] = await get_result(user=email, draft=draft_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
