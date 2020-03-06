from collections import defaultdict

from promise import Promise
from promise.dataloader import DataLoader

from backend.domain import event as event_domain


def _batch_load_fn(event_ids):
    """Batch the data load requests within the same execution fragment."""
    events = defaultdict(list)

    for event in event_domain.get_events(event_ids):
        history = event.get('historic_state', [])
        events[event['event_id']] = {
            'accessibility': event.get('accessibility', ''),
            'affectation': history[-1].get('affectation', ''),
            'affected_components': event.get('affected_components', ''),
            'analyst': event.get('analyst', ''),
            'client': event.get('client', ''),
            'client_project': event.get('client_project', ''),
            'closing_date': event.get('closing_date', '-'),
            'context': event.get('context', ''),
            'detail': event.get('detail', ''),
            'event_date': history[0].get('date', ''),
            'evidence_file': event.get('evidence_file', ''),
            'event_status': history[-1].get('state', ''),
            'event_type': event.get('event_type', ''),
            'evidence': event.get('evidence', ''),
            'historic_state': history,
            'id': event.get('event_id', ''),
            'project_name': event.get('project_name', ''),
            'subscription': event.get('subscription', '')
        }

    return Promise.resolve([events.get(event_id, [])
                            for event_id in event_ids])


class EventLoader(DataLoader):
    def __init__(self):
        super(EventLoader, self).__init__(batch_load_fn=_batch_load_fn)
