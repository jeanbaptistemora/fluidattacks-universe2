# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .types import (
    StakeholderMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def update_metadata(
    *,
    email: str,
    metadata: StakeholderMetadataToUpdate,
) -> None:
    email = email.strip().lower()
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": email,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={
            "all": "all",
            "email": email,
        },
    )
    item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        "email": email,
        **format_metadata_item(metadata),
    }
    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )
