# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    await operations.delete_item(key=primary_key, table=TABLE)
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
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[TABLE.primary_key.partition_key],
                sort_key=item[TABLE.primary_key.sort_key],
            )
            for item in response_historics.items
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
