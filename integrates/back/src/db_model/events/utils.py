from .types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventMetadataToUpdate,
    EventState,
    EventUnreliableIndicators,
    EventUnreliableIndicatorsToUpdate,
)
from datetime import (
    datetime,
)
from db_model.events.enums import (
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from db_model.groups.types import (
    Group,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


def filter_events_not_in_groups(
    *,
    groups: list[Group],
    events: list[Event],
) -> list[Event]:
    return [
        event
        for event in events
        if event.group_name not in set(group.name for group in groups)
    ]


def format_evidences(evidences: Item) -> EventEvidences:
    return EventEvidences(
        file_1=EventEvidence(
            file_name=evidences["file_1"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["file_1"]["modified_date"]
            ),
        )
        if evidences.get("file_1")
        else None,
        image_1=EventEvidence(
            file_name=evidences["image_1"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_1"]["modified_date"]
            ),
        )
        if evidences.get("image_1")
        else None,
        image_2=EventEvidence(
            file_name=evidences["image_2"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_2"]["modified_date"]
            ),
        )
        if evidences.get("image_2")
        else None,
        image_3=EventEvidence(
            file_name=evidences["image_3"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_3"]["modified_date"]
            ),
        )
        if evidences.get("image_3")
        else None,
        image_4=EventEvidence(
            file_name=evidences["image_4"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_4"]["modified_date"]
            ),
        )
        if evidences.get("image_4")
        else None,
        image_5=EventEvidence(
            file_name=evidences["image_5"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_5"]["modified_date"]
            ),
        )
        if evidences.get("image_5")
        else None,
        image_6=EventEvidence(
            file_name=evidences["image_6"]["file_name"],
            modified_date=datetime.fromisoformat(
                evidences["image_6"]["modified_date"]
            ),
        )
        if evidences.get("image_6")
        else None,
    )


def format_event(item: Item) -> Event:
    return Event(
        client=item["client"],
        created_by=item["created_by"],
        created_date=datetime.fromisoformat(item["created_date"]),
        description=item["description"],
        event_date=datetime.fromisoformat(item["event_date"]),
        evidences=format_evidences(item["evidences"]),
        group_name=item["group_name"],
        hacker=item["hacker"],
        id=item["id"],
        root_id=item.get("root_id"),
        state=EventState(
            comment_id=item["state"].get("comment_id"),
            modified_by=item["state"]["modified_by"],
            modified_date=datetime.fromisoformat(
                item["state"]["modified_date"]
            ),
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
        "created_by": event.created_by,
        "created_date": get_as_utc_iso_format(event.created_date),
        "description": event.description,
        "event_date": get_as_utc_iso_format(event.event_date),
        "evidences": json.loads(
            json.dumps(event.evidences, default=serialize)
        ),
        "group_name": event.group_name,
        "hacker": event.hacker,
        "id": event.id,
        "state": json.loads(json.dumps(event.state, default=serialize)),
        "type": event.type.value,
        "root_id": event.root_id,
        "unreliable_indicators": json.loads(
            json.dumps(event.unreliable_indicators, default=serialize)
        ),
    }


def format_metadata_item(metadata: EventMetadataToUpdate) -> Item:
    item = {
        "client": metadata.client,
        "description": metadata.description,
        "root_id": metadata.root_id,
        "type": metadata.type,
    }
    return {key: value for key, value in item.items() if value is not None}


def format_state(item: Item) -> EventState:
    return EventState(
        modified_by=item["modified_by"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
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
        unreliable_solving_date=datetime.fromisoformat(
            item["unreliable_solving_date"]
        )
        if item.get("unreliable_solving_date")
        else None,
    )


def format_unreliable_indicators_to_update_item(
    indicators: EventUnreliableIndicatorsToUpdate,
) -> Item:
    item = {
        "unreliable_solving_date": (
            get_as_utc_iso_format(indicators.unreliable_solving_date)
            if indicators.unreliable_solving_date
            else None
        ),
    }
    item = {key: value for key, value in item.items() if value is not None}

    if indicators.clean_unreliable_solving_date:
        item["unreliable_solving_date"] = None

    return item
