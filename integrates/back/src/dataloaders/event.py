from aiodataloader import (
    DataLoader,
)
from collections import (
    defaultdict,
)
from db_model.events.types import (
    Event,
)
from dynamodb.types import (
    Item,
)
from events import (
    dal as events_dal,
    domain as events_domain,
)
from newutils.events import (
    format_event,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Iterable,
)


async def _batch_load_fn(event_ids: list[str]) -> list[dict[str, Any]]:
    """Batch the data load requests within the same execution fragment."""
    events: dict[str, dict[str, Any]] = defaultdict(dict[str, Any])

    evnts = await events_domain.get_events(event_ids)
    for event in evnts:
        history: list[dict[str, str]] = event.get("historic_state", [])
        event_id: str = event["event_id"]
        client_group = str(
            event.get("client_group", event.get("client_project", ""))
        )
        group_name: str = get_key_or_fallback(event, fallback="")
        events[event_id] = dict(
            accessibility=event.get("accessibility", ""),
            action_after_blocking=event.get("action_after_blocking", "NONE"),
            action_before_blocking=event.get("action_before_blocking", "NONE"),
            affected_components=event.get("affected_components", ""),
            analyst=event.get("analyst", ""),
            client=event.get("client", ""),
            closing_date=event.get("closing_date", "-"),
            context=event.get("context", ""),
            detail=event.get("detail", ""),
            event_date=history[0].get("date", ""),
            evidence_date=(
                event["evidence_date"] if "evidence" in event else ""
            ),
            evidence_file=event.get("evidence_file", ""),
            evidence_file_date=(
                event["evidence_file_date"] if "evidence_file" in event else ""
            ),
            event_status=history[-1].get("state", ""),
            event_type=event.get("event_type", ""),
            evidence=event.get("evidence", ""),
            historic_state=history,
            id=event.get("event_id", ""),
            subscription=event.get("subscription", ""),
            # Compatibility with old API
            client_group=client_group,
            client_project=client_group,
            project_name=group_name,
            group_name=group_name,
        )
    return [events.get(event_id, {}) for event_id in event_ids]


class EventLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, event_ids: list[str]
    ) -> list[dict[str, Any]]:
        return await _batch_load_fn(event_ids)


class EventTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, event_ids: Iterable[str]
    ) -> tuple[Event, ...]:
        event_items: list[Item] = [
            await events_dal.get_event(id) for id in event_ids
        ]
        return tuple(format_event(item) for item in event_items)
