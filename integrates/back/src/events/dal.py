from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    EventNotFound,
    UnavailabilityError,
)
from db_model.events.enums import (
    EventEvidenceType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventMetadataToUpdate,
    EventState,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    events as events_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = "fi_events"


async def add(
    event_id: str, group_name: str, event_attributes: dict[str, Any]
) -> bool:
    success = False
    try:
        event_attributes.update(
            {"event_id": event_id, "project_name": group_name}
        )
        success = await dynamodb_ops.put_item(TABLE_NAME, event_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def add_typed(
    *,
    event: Event,
) -> None:
    item = events_utils.format_event_item(event)
    if not await dynamodb_ops.put_item(TABLE_NAME, item):
        raise UnavailabilityError()


async def get_event(event_id: str) -> dict[str, Any]:
    """Retrieve all attributes from an event"""
    response = {}
    query_attrs = {
        "KeyConditionExpression": Key("event_id").eq(event_id),
        "Limit": 1,
    }
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if not response_items:
        raise EventNotFound()
    response = response_items[0]
    # Compatibility with old API
    response["group_name"] = response["project_name"]
    return response


async def list_group_events(group_name: str) -> list[str]:
    key_exp = Key("project_name").eq(group_name)
    query_attrs = {
        "KeyConditionExpression": key_exp,
        "IndexName": "project_events",
        "ProjectionExpression": "event_id",
    }
    events = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    return [event["event_id"] for event in events]


async def update(event_id: str, data: dict[str, Any]) -> bool:
    success = False
    set_expression = ""
    remove_expression = ""
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"{attr}, "
        else:
            set_expression += f"{attr} = :{attr}, "
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {"event_id": event_id},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def update_state(
    *,
    event_id: str,
    group_name: str,
    state: EventState,
) -> None:
    event_item = await get_event(event_id=event_id)
    current_historic = event_item["historic_state"]
    state_to_add = events_utils.format_state_item(state)
    historic_state = [*current_historic, state_to_add]
    if not await update(
        event_id=event_id,
        data={"historic_state": historic_state, "project_name": group_name},
    ):
        raise UnavailabilityError()


async def update_evidence(
    *,
    event_id: str,
    group_name: str,
    evidence_info: Optional[EventEvidence],
    evidence_type: EventEvidenceType,
) -> None:
    evidence_type_str = (
        "evidence"
        if evidence_type == EventEvidenceType.IMAGE
        else "evidence_file"
    )
    item = {
        evidence_type_str: evidence_info.file_name if evidence_info else None,
        f"{evidence_type_str}_date": datetime_utils.convert_from_iso_str(
            evidence_info.modified_date
        )
        if evidence_info
        else None,
        "project_name": group_name,
    }
    if not await update(
        event_id=event_id,
        data=item,
    ):
        raise UnavailabilityError()


async def update_metadata(
    *,
    event_id: str,
    group_name: str,
    metadata: EventMetadataToUpdate,
) -> None:
    item = events_utils.format_metadata_item(metadata)
    if not await update(
        event_id=event_id,
        data={
            **item,
            "project_name": group_name,
        },
    ):
        raise UnavailabilityError()
