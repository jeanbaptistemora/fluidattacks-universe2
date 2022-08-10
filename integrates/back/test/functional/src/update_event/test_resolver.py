from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventAffectedComponents,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event")
@pytest.mark.parametrize(
    ["email", "event_id", "event_type", "affected_components"],
    [
        ["admin@gmail.com", "418900971", "AUTHORIZATION_SPECIAL_ATTACK", []],
        ["admin@gmail.com", "418900972", "DATA_UPDATE_REQUIRED", None],
        ["admin@gmail.com", "418900974", "OTHER", None],
        ["admin@gmail.com", "418900974", "TOE_DIFFERS_APPROVED", []],
        ["admin@gmail.com", "418900975", "OTHER", []],
    ],
)
async def test_update_event(
    populate: bool,
    email: str,
    event_id: str,
    event_type: str,
    affected_components: list[str],
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.SOLVED

    result: dict[str, Any] = await get_result(
        user=email,
        event_id=event_id,
        event_type=event_type,
        affected_components=affected_components,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateEvent"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event.type == EventType[event_type]
    if affected_components:
        assert sorted(event.affected_components) == sorted(
            [
                EventAffectedComponents[affected_component]
                for affected_component in affected_components
            ]
        )
    else:
        assert event.affected_components is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event")
@pytest.mark.parametrize(
    ["email", "event_id", "event_type", "affected_components"],
    [
        ["user@gmail.com", "418900971", "AUTHORIZATION_SPECIAL_ATTACK", []],
        ["reviewer@gmail.com", "418900972", "DATA_UPDATE_REQUIRED", None],
    ],
)
async def test_update_event_fail(
    populate: bool,
    email: str,
    event_id: str,
    event_type: str,
    affected_components: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        event_id=event_id,
        event_type=event_type,
        affected_components=affected_components,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
