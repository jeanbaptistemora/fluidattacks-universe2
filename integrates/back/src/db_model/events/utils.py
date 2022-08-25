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
        file_1=EventEvidence(
            file_name=evidences["file_1"]["file_name"],
            modified_date=evidences["file_1"]["modified_date"],
        )
        if evidences.get("file_1")
        else None,
        image_1=EventEvidence(
            file_name=evidences["image_1"]["file_name"],
            modified_date=evidences["image_1"]["modified_date"],
        )
        if evidences.get("image_1")
        else None,
        image_2=EventEvidence(
            file_name=evidences["image_2"]["file_name"],
            modified_date=evidences["image_2"]["modified_date"],
        )
        if evidences.get("image_2")
        else None,
        image_3=EventEvidence(
            file_name=evidences["image_3"]["file_name"],
            modified_date=evidences["image_3"]["modified_date"],
        )
        if evidences.get("image_3")
        else None,
        image_4=EventEvidence(
            file_name=evidences["image_4"]["file_name"],
            modified_date=evidences["image_4"]["modified_date"],
        )
        if evidences.get("image_4")
        else None,
        image_5=EventEvidence(
            file_name=evidences["image_5"]["file_name"],
            modified_date=evidences["image_5"]["modified_date"],
        )
        if evidences.get("image_5")
        else None,
        image_6=EventEvidence(
            file_name=evidences["image_6"]["file_name"],
            modified_date=evidences["image_6"]["modified_date"],
        )
        if evidences.get("image_6")
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
            comment_id=item["state"].get("comment_id"),
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
