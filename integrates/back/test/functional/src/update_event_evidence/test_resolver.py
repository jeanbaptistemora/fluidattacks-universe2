from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    Event,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
async def test_admin(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["updateEventEvidence"]
    assert result["data"]["updateEventEvidence"]["success"]

    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert (
        event.evidences.image_1.file_name  # type: ignore
        == "group1_418900971_evidence_image_1.gif"
    )
    assert event.evidences.file_1 is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@fluidattacks.com"],
    ],
)
async def test_access_denied(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
