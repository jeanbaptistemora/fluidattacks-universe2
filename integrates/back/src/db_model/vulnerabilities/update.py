from .enums import (
    VulnerabilityStateStatus,
)
from .types import (
    VulnerabilityHistoric,
    VulnerabilityHistoricEntry,
    VulnerabilityMetadataToUpdate,
)
from .utils import (
    historic_entry_type_to_str,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    VulnNotFound,
)
from db_model import (
    TABLE,
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


async def update_metadata(
    *,
    finding_id: str,
    metadata: VulnerabilityMetadataToUpdate,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "id": vulnerability_id},
    )
    vulnerability_item = {
        key: None if not value else value
        for key, value in json.loads(json.dumps(metadata)).items()
        if value is not None
    }
    if vulnerability_item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=vulnerability_item,
                key=vulnerability_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise VulnNotFound() from ex


async def update_historic_entry(
    *,
    current_entry: Optional[VulnerabilityHistoricEntry],
    finding_id: str,
    entry: VulnerabilityHistoricEntry,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    entry_type = historic_entry_type_to_str(entry)
    entry_item = json.loads(json.dumps(entry))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {entry_type: entry_item}
        base_condition = Attr("state.status").ne(
            VulnerabilityStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr(f"{entry_type}.modified_date").eq(
                    current_entry.modified_date
                )
                if current_entry
                else base_condition
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_entry_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={
            "id": vulnerability_id,
            "iso8601utc": entry.modified_date,
        },
    )
    historic_item = {
        key_structure.partition_key: historic_entry_key.partition_key,
        key_structure.sort_key: historic_entry_key.sort_key,
        **entry_item,
    }
    await operations.put_item(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        item=historic_item,
        table=TABLE,
    )


async def update_historic(
    *,
    finding_id: str,
    historic: VulnerabilityHistoric,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    latest_entry = historic[-1]
    entry_type = historic_entry_type_to_str(latest_entry)

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {entry_type: json.loads(json.dumps(latest_entry))}
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets[f"vulnerability_historic_{entry_type}"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["sk"].split("#")[1],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": entry.modified_date,
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )
