# pylint: disable=method-hidden

from collections import defaultdict

from typing import Dict, List, cast
from backend.domain import event as event_domain
from backend.typing import Event as EventType, Historic
from aiodataloader import DataLoader


async def _batch_load_fn(event_ids: List[str]) -> List[EventType]:
    """Batch the data load requests within the same execution fragment."""
    events: Dict[str, EventType] = defaultdict(EventType)

    evnts = await event_domain.get_events(event_ids)
    for event in evnts:
        history: Historic = cast(Historic, event.get('historic_state', []))
        event_id: str = cast(str, event['event_id'])
        events[event_id] = dict(
            accessibility=event.get('accessibility', ''),
            affectation=history[-1].get('affectation', ''),
            affected_components=event.get('affected_components', ''),
            analyst=event.get('analyst', ''),
            client=event.get('client', ''),
            client_project=event.get('client_project', ''),
            closing_date=event.get('closing_date', '-'),
            context=event.get('context', ''),
            detail=event.get('detail', ''),
            event_date=history[0].get('date', ''),
            evidence_file=event.get('evidence_file', ''),
            event_status=history[-1].get('state', ''),
            event_type=event.get('event_type', ''),
            evidence=event.get('evidence', ''),
            historic_state=history,
            id=event.get('event_id', ''),
            project_name=event.get('project_name', ''),
            subscription=event.get('subscription', '')
        )

    return [events.get(event_id, dict()) for event_id in event_ids]


# pylint: disable=too-few-public-methods
class EventLoader(DataLoader):
    async def batch_load_fn(self, event_ids: List[str]) -> List[EventType]:
        return await _batch_load_fn(event_ids)
