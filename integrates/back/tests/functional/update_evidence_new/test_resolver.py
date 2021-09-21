from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_new")
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
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(user=email, draft=finding_id)
    assert "errors" not in result
    assert "success" in result["data"]["updateEvidence"]
    assert result["data"]["updateEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["executive@gmail.com"],
    ],
)
async def test_update_evidence_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(user=email, draft=finding_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
