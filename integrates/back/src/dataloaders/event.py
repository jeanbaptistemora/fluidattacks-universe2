# pylint: disable=method-hidden
from aiodataloader import (
    DataLoader,
)
from collections import (
    defaultdict,
)
from custom_types import (
    Event as EventType,
    Historic,
)
from events import (
    domain as events_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    cast,
    Dict,
    List,
)


async def _batch_load_fn(event_ids: List[str]) -> List[EventType]:
    """Batch the data load requests within the same execution fragment."""
    events: Dict[str, EventType] = defaultdict(EventType)

    evnts = await events_domain.get_events(event_ids)
    for event in evnts:
        history: Historic = cast(Historic, event.get("historic_state", []))
        event_id: str = cast(str, event["event_id"])
        client_group: str = event.get(
            "client_group", event.get("client_project", "")
        )
        group_name: str = get_key_or_fallback(event, fallback="")
        events[event_id] = dict(
            accessibility=event.get("accessibility", ""),
            action_after_blocking=event.get("action_after_blocking", "NONE"),
            action_before_blocking=event.get("action_before_blocking", "NONE"),
            affectation=history[-1].get("affectation", ""),
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
    # pylint: disable=no-self-use
    async def batch_load_fn(self, event_ids: List[str]) -> List[EventType]:
        return await _batch_load_fn(event_ids)
