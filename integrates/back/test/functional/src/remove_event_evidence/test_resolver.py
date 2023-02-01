from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
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
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["removeEventEvidence"]
    assert result["data"]["removeEventEvidence"]["success"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event
    assert event.evidences.image_1 is None
    assert event.evidences.file_1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_event_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_remove_event_evidence_fail(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900972"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
