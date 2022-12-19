from .types import (
    Event,
    EventEvidence,
    EventMetadataToUpdate,
    EventState,
    EventUnreliableIndicatorsToUpdate,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    EventNotFound,
    IndicatorAlreadyUpdated,
)
from db_model import (
    TABLE,
)
from db_model.events.constants import (
    GSI_2_FACET,
)
from db_model.events.enums import (
    EventEvidenceId,
    EventStateStatus,
)
from db_model.events.utils import (
    format_metadata_item,
    format_unreliable_indicators_to_update_item,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json
from typing import (
    Optional,
)


async def update_evidence(
    *,
    event_id: str,
    group_name: str,
    evidence_info: Optional[EventEvidence],
    evidence_id: EventEvidenceId,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={"id": event_id, "name": group_name},
    )
    attribute = f"evidences.{str(evidence_id.value).lower()}"
    await operations.update_item(
        item={
            attribute: json.loads(json.dumps(evidence_info, default=serialize))
            if evidence_info
            else None
        },
        key=primary_key,
        table=TABLE,
    )


async def update_metadata(
    *,
    event_id: str,
    group_name: str,
    metadata: EventMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event_id,
            "name": group_name,
        },
    )
    item = format_metadata_item(metadata)
    if item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=item,
                key=primary_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise EventNotFound() from ex


async def update_state(
    *,
    current_value: Event,
    group_name: str,
    state: EventState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state, default=serialize))
    gsi_2_index = TABLE.indexes["gsi_2"]

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["event_metadata"],
            values={
                "id": current_value.id,
                "name": group_name,
            },
        )
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "is_solved": str(
                    state.status is EventStateStatus.SOLVED
                ).lower(),
                "group_name": group_name,
            },
        )
        item = {
            "state": state_item,
            gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
            gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        }
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.modified_date").eq(
            get_as_utc_iso_format(current_value.state.modified_date)
        )
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
            "id": current_value.id,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
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


async def update_unreliable_indicators(
    *,
    current_value: Event,
    indicators: EventUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": current_value.id,
            "name": current_value.group_name,
        },
    )
    unreliable_indicators_item = {
        f"unreliable_indicators.{key}": value
        for key, value in format_unreliable_indicators_to_update_item(
            indicators
        ).items()
    }
    current_indicators_item = {
        f"unreliable_indicators.{key}": value
        for key, value in json.loads(
            json.dumps(current_value.unreliable_indicators, default=serialize),
            parse_float=Decimal,
        ).items()
        if value is not None
    }

    conditions = (
        Attr(indicator_name).eq(current_indicators_item[indicator_name])
        for indicator_name in unreliable_indicators_item
        if indicator_name in current_indicators_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        if unreliable_indicators_item:
            await operations.update_item(
                condition_expression=condition_expression,
                item=unreliable_indicators_item,
                key=primary_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex
