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
    response_index = await operations.query(
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

    response_historics = await operations.query(
        condition_expression=(
            Key(TABLE.primary_key.partition_key).eq(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets["finding_historic_state"],
            TABLE.facets["finding_historic_verification"],
        ),
        table=TABLE,
    )

    primary_key_removed = keys.build_key(
        facet=TABLE.facets["removed_finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    response_removed = await operations.query(
        condition_expression=(
            Key(index.primary_key.partition_key).eq(
                primary_key_removed.sort_key
            )
            & Key(index.primary_key.sort_key).begins_with(
                primary_key_removed.partition_key
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

    items = set(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response_index.items
        + response_historics.items
        + response_removed.items
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item.partition_key,
                sort_key=item.sort_key,
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
