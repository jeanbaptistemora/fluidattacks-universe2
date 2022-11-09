# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Group,
)
from .utils import (
    serialize_sets,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    GroupAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


async def add(*, group: Group) -> None:
    # Currently, a prefix could precede the organization id, let's remove it
    group = group._replace(
        organization_id=remove_org_id_prefix(group.organization_id)
    )

    key_structure = TABLE.primary_key
    id_key = keys.build_key(
        facet=TABLE.facets["group_id"],
        values={"name": group.name},
    )
    id_item = {
        key_structure.partition_key: id_key.partition_key,
        key_structure.sort_key: id_key.sort_key,
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["group_id"],
            item=id_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise GroupAlreadyCreated() from ex

    items: list[Item] = []
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={
            "name": group.name,
            "organization_id": group.organization_id,
        },
    )
    metadata_item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(group, default=serialize_sets)),
    }
    items.append(metadata_item)
    state_key = keys.build_key(
        facet=TABLE.facets["group_historic_state"],
        values={
            "name": group.name,
            "iso8601utc": group.state.modified_date,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(group.state, default=serialize_sets)),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
