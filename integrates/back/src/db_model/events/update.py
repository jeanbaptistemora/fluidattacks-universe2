from .types import (
    EventEvidence,
    EventState,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    EventNotFound,
)
from db_model import (
    TABLE,
)
from db_model.events.enums import (
    EventEvidenceType,
    EventStateStatus,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore
from typing import (
    Optional,
)


async def update_evidence(
    *,
    event_id: str,
    group_name: str,
    evidence_info: Optional[EventEvidence],
    evidence_type: EventEvidenceType,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={"id": event_id, "name": group_name},
    )
    attribute = f"evidences.{str(evidence_type.value).lower()}"
    await operations.update_item(
        item={
            attribute: json.loads(json.dumps(evidence_info))
            if evidence_info
            else None
        },
        key=primary_key,
        table=TABLE,
    )


async def update_state(
    *,
    event_id: str,
    group_name: str,
    state: EventState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state))

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["event_metadata"],
            values={
                "id": event_id,
                "name": group_name,
            },
        )
        item = {"state": state_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.status").ne(EventStateStatus.SOLVED.value)
        await operations.update_item(
            condition_expression=condition_expression,
            item=item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise EventNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["event_historic_state"],
        values={
            "id": event_id,
            "iso8601utc": state.modified_date,
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["event_historic_state"],
        item=historic_item,
        table=TABLE,
    )
