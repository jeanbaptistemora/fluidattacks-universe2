from .types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventMetadataToUpdate,
    EventState,
    EventUnreliableIndicators,
)
from db_model.events.enums import (
    EventActionsAfterBlocking,
    EventActionsBeforeBlocking,
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from dynamodb.types import (
    Item,
)
import simplejson as json  # type: ignore


def format_evidences(evidences: Item) -> EventEvidences:
    return EventEvidences(
        file=EventEvidence(
            file_name=evidences["file"]["file_name"],
            modified_date=evidences["file"]["modified_date"],
        )
        if evidences.get("file")
        else None,
        image=EventEvidence(
            file_name=evidences["image"]["file_name"],
            modified_date=evidences["image"]["modified_date"],
        )
        if evidences.get("image")
        else None,
    )


def format_event(item: Item) -> Event:
    return Event(
        action_after_blocking=EventActionsAfterBlocking[
            item["action_after_blocking"]
        ]
        if item.get("action_after_blocking")
        else None,
        action_before_blocking=EventActionsBeforeBlocking[
            item["action_before_blocking"]
        ]
        if item.get("action_before_blocking")
        else None,
        client=item["client"],
        context=item.get("context"),
        description=item["description"],
        event_date=item["event_date"],
        evidences=format_evidences(item["evidences"]),
        group_name=item["group_name"],
        hacker=item["hacker"],
        id=item["id"],
        root_id=item.get("root_id"),
        state=EventState(
            modified_by=item["state"]["modified_by"],
            modified_date=item["state"]["modified_date"],
            status=EventStateStatus[item["state"]["status"]],
            other=item["state"].get("other"),
            reason=EventSolutionReason[item["state"]["reason"]]
            if item["state"].get("reason")
            else None,
        ),
        type=EventType[item["type"]],
        unreliable_indicators=format_unreliable_indicators(
            item["unreliable_indicators"]
        ),
    )


def format_event_item(event: Event) -> Item:
    return {
        "client": event.client,
        "description": event.description,
        "event_date": event.event_date,
        "evidences": json.loads(json.dumps(event.evidences)),
        "group_name": event.group_name,
        "hacker": event.hacker,
        "id": event.id,
        "state": json.loads(json.dumps(event.state)),
        "type": event.type.value,
        "action_after_blocking": event.action_after_blocking.value
        if event.action_after_blocking
        else None,
        "action_before_blocking": event.action_before_blocking.value
        if event.action_before_blocking
        else None,
        "context": event.context,
        "root_id": event.root_id,
        "unreliable_indicators": json.loads(
            json.dumps(event.unreliable_indicators)
        ),
    }


def format_metadata_item(metadata: EventMetadataToUpdate) -> Item:
    item = {
        "client": metadata.client,
        "description": metadata.description,
        "type": metadata.type,
    }
    return {key: value for key, value in item.items() if value is not None}


def format_state(item: Item) -> EventState:
    return EventState(
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=EventStateStatus[item["status"]],
        other=item.get("other"),
        reason=EventSolutionReason[item["reason"]]
        if item.get("reason")
        else None,
    )


def format_unreliable_indicators(
    item: Item,
) -> EventUnreliableIndicators:
    return EventUnreliableIndicators(
        unreliable_solving_date=item.get("unreliable_solving_date"),
    )
