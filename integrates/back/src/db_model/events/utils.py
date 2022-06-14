from .types import (
    Event,
)
from dynamodb.types import (
    Item,
)
import simplejson as json  # type: ignore


def format_event_item(event: Event) -> Item:
    return {
        "client": event.client,
        "description": event.description,
        "evidences": json.loads(json.dumps(event.evidences)),
        "group_name": event.group_name,
        "hacker": event.hacker,
        "id": event.id,
        "report_date": event.report_date,
        "state": json.loads(json.dumps(event.state)),
        "type": event.type.value,
        "accessibility": set(
            acc_item.value for acc_item in event.accessibility
        )
        if event.accessibility
        else None,
        "action_after_blocking": event.action_after_blocking.value
        if event.action_after_blocking
        else None,
        "action_before_blocking": event.action_before_blocking.value
        if event.action_before_blocking
        else None,
        "affected_components": set(
            acc_item.value for acc_item in event.affected_components
        )
        if event.affected_components
        else None,
        "context": event.context,
        "root_id": event.root_id,
    }
