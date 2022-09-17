# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.credentials.constants import (
    OWNER_INDEX_FACET,
)
from db_model.credentials.types import (
    CredentialsState,
)
from db_model.credentials.utils import (
    validate_secret,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json


async def update_credential_state(
    *,
    current_value: CredentialsState,
    organization_id: str,
    credential_id: str,
    state: CredentialsState,
    force_update_owner: bool = False,
) -> None:
    validate_secret(state)
    key_structure = TABLE.primary_key
    credential_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={
            "organization_id": organization_id,
            "id": credential_id,
        },
    )
    state_item = json.loads(json.dumps(state))
    credential_item = {"state": state_item}
    if force_update_owner or current_value.secret != state.secret:
        gsi_2_index = TABLE.indexes["gsi_2"]
        gsi_2_key = keys.build_key(
            facet=OWNER_INDEX_FACET,
            values={
                "owner": state.modified_by,
                "id": credential_id,
            },
        )
        credential_item.update(
            {
                "owner": state.modified_by,
                gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
                gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
            }
        )
    await operations.update_item(
        condition_expression=(
            Attr(key_structure.partition_key).exists()
            & Attr("state.modified_date").eq(current_value.modified_date)
        ),
        item=credential_item,
        key=credential_key,
        table=TABLE,
    )
