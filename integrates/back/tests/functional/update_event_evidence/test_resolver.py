from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
async def test_admin(populate: bool) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(
        user="admin@gmail.com", event=event_id
    )
    assert result["data"]["updateEventEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
async def test_analyst(populate: bool) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(
        user="analyst@gmail.com", event=event_id
    )
    assert result["data"]["updateEventEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
async def test_closer(populate: bool) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(
        user="closer@gmail.com", event=event_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
