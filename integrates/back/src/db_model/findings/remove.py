from .enums import (
    FindingEvidenceName,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, group_name: str, finding_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    index = TABLE.indexes["inverted_index"]
    items = await operations.query(
        condition_expression=(
            Key(index.primary_key.partition_key).eq(primary_key.sort_key)
            & Key(index.primary_key.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["finding_approval"],
            TABLE.facets["finding_creation"],
            TABLE.facets["finding_metadata"],
            TABLE.facets["finding_state"],
            TABLE.facets["finding_submission"],
            TABLE.facets["finding_unreliable_indicators"],
            TABLE.facets["finding_verification"],
        ),
        index=index,
        table=TABLE,
    )

    await operations.batch_write_item(
        items=tuple(
            {
                **item,
                TABLE.primary_key.partition_key: (
                    f"REMOVED#{item[TABLE.primary_key.partition_key]}"
                ),
            }
            for item in items
        ),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[TABLE.primary_key.partition_key],
                sort_key=item[TABLE.primary_key.sort_key],
            )
            for item in items
        ),
        table=TABLE,
    )


async def remove_evidence(
    *,
    evidence_name: FindingEvidenceName,
    finding_id: str,
    group_name: str,
) -> None:
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    attribute = f"evidences.{evidence_name.value}"
    await operations.update_item(
        condition_expression=Attr(attribute).exists(),
        item={attribute: None},
        key=metadata_key,
        table=TABLE,
    )
