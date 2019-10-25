from collections import defaultdict

from promise import Promise
from promise.dataloader import DataLoader

from app.domain import event as event_domain
from app.entity.event import Event


def _batch_load_fn(event_ids):
    """Batches the data load requests within the same execution fragment"""
    events = defaultdict(list)

    for event in event_domain.get_events(event_ids):
        events[event['event_id']] = Event(
            accessibility=event.get('accessibility', ''),
            affectation=event.get('affectation', ''),
            affected_components=event.get('affected_components', ''),
            analyst=event.get('analyst', ''),
            client=event.get('client', ''),
            client_project=event.get('client_project', ''),
            context=event.get('context', ''),
            detail=event.get('detail', ''),
            event_date=event.get('event_date', ''),
            evidence_file=event.get('evidence', ''),
            event_status=event.get('event_status', ''),
            event_type=event.get('event_type', ''),
            evidence=event.get('evidence', ''),
            id=event.get('event_id', ''),
            project_name=event.get('project_name', ''),
            subscription=event.get('subscription', '')
        )

    return Promise.resolve([events.get(event_id, [])
                            for event_id in event_ids])


class EventLoader(DataLoader):
    def __init__(self):
        super(EventLoader, self).__init__(batch_load_fn=_batch_load_fn)
