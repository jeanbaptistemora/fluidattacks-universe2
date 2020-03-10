from typing import Dict, List, cast
from backend.dal.event import EventType


def format_data(event: EventType) -> EventType:
    historic_state = cast(List[Dict[str, str]], event.get('historic_state', [{}, {}]))
    event['closing_date'] = '-'
    if historic_state[-1].get('state') == 'SOLVED':
        event['closing_date'] = historic_state[-2].get('date', '')

    return event
