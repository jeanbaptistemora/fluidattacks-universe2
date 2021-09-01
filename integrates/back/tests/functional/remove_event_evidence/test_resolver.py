from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_event_evidence")
@pytest.mark.parametrize(
    ["email", "event_id"],
    [
        ["admin@gmail.com", "418900971"],
        ["hacker@gmail.com", "418900972"],
    ],
)
async def test_remove_event_evidence(
    populate: bool, email: str, event_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, event=event_id)
    assert result["data"]["removeEventEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_event_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_remove_event_evidence_fail(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900972"
    result: Dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
