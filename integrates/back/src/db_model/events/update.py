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
from db_model.events.enums import (
    EventEvidenceType,
)
from db_model.events.utils import (
    format_metadata_item,
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
    state_item = json.loads(json.dumps(state))

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["event_metadata"],
            values={
                "id": current_value.id,
                "name": group_name,
            },
        )
        item = {"state": state_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.modified_date").eq(
            current_value.state.modified_date
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
    unreliable_indicators = {
        f"unreliable_indicators.{key}": Decimal(str(value))
        if isinstance(value, float)
        else value
        for key, value in json.loads(json.dumps(indicators)).items()
        if value is not None
    }
    current_value_item = {
        f"unreliable_indicators.{key}": Decimal(str(value))
        if isinstance(value, float)
        else value
        for key, value in json.loads(
            json.dumps(current_value.unreliable_indicators)
        ).items()
    }
    conditions = (
        (
            Attr(indicator_name).not_exists()
            | Attr(indicator_name).eq(current_value_item[indicator_name])
        )
        for indicator_name in unreliable_indicators
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        if unreliable_indicators:
            await operations.update_item(
                condition_expression=condition_expression,
                item=unreliable_indicators,
                key=primary_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex
