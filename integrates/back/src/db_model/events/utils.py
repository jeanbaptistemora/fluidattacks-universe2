from .types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventMetadataToUpdate,
    EventState,
)
from db_model.events.enums import (
    EventAccessibility,
    EventActionsAfterBlocking,
    EventActionsBeforeBlocking,
    EventAffectedComponents,
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
        accessibility=set(
            EventAccessibility[acc_item] for acc_item in item["accessibility"]
        )
        if item.get("accessibility")
        else None,
        affected_components=set(
            EventAffectedComponents[aff_item]
            for aff_item in item["affected_components"]
        )
        if item.get("affected_components")
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
        ),
        type=EventType[item["type"]],
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


def format_metadata_item(metadata: EventMetadataToUpdate) -> Item:
    item = {
        "client": metadata.client,
        "description": metadata.description,
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
