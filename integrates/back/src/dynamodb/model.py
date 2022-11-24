from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from context import (
    FI_DB_MODEL_PATH,
)
from custom_exceptions import (
    OrgFindingPolicyNotFound,
)
from dynamodb import (
    keys,
    operations,
    tables,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
    PrimaryKey,
)
from itertools import (
    chain,
)
import json

with open(FI_DB_MODEL_PATH, mode="r", encoding="utf-8") as file:
    TABLE = tables.load_tables(json.load(file))[0]


def _build_org_policy_finding(
    item: Item,
) -> OrgFindingPolicyItem:
    key_structure = TABLE.primary_key
    return OrgFindingPolicyItem(
        id=item[key_structure.partition_key].split("#")[1],
        org_name=item[key_structure.sort_key].split("#")[1],
        metadata=OrgFindingPolicyMetadata(
            name=item["name"], tags=item.get("tags", {})
        ),
        state=OrgFindingPolicyState(
            modified_by=item["state"]["modified_by"],
            modified_date=item["state"]["modified_date"],
            status=item["state"]["status"],
        ),
    )


async def get_org_finding_policies(
    *, org_name: str
) -> tuple[OrgFindingPolicyItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["org_finding_policy_metadata"],),
        index=index,
        table=TABLE,
    )

    return tuple(_build_org_policy_finding(item) for item in response.items)


async def add_organization_finding_policy(
    *, finding_policy: OrgFindingPolicyItem
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={
            "name": finding_policy.org_name,
            "uuid": finding_policy.id,
        },
    )
    items: list[Item] = []
    metadata_item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        "name": finding_policy.metadata.name,
        "state": dict(finding_policy.state._asdict()),
        "tags": finding_policy.metadata.tags,
    }
    items.append(metadata_item)
    state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        values={
            "iso8601utc": finding_policy.state.modified_date,
            "uuid": finding_policy.id,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **dict(finding_policy.state._asdict()),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)


async def update_organization_finding_policy_state(
    *, org_name: str, finding_policy_id: str, state: OrgFindingPolicyState
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name, "uuid": finding_policy_id},
    )
    item = {
        "state": dict(state._asdict()),
    }
    try:
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise OrgFindingPolicyNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        values={
            "iso8601utc": state.modified_date,
            "uuid": finding_policy_id,
        },
    )
    historic_state_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **dict(state._asdict()),
    }
    await operations.put_item(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        item=historic_state_item,
        table=TABLE,
    )


async def _get_historic_state_items(*, policy_id: str) -> tuple[Item, ...]:
    facet = TABLE.facets["org_finding_policy_historic_state"]
    primary_key = keys.build_key(
        facet=facet,
        values={"uuid": policy_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(facet,),
        table=TABLE,
    )

    return response.items


async def remove_org_finding_policies(*, organization_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": organization_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["org_finding_policy_metadata"],),
        index=index,
        table=TABLE,
    )
    if not response.items:
        return

    policies_ids = set(
        item[TABLE.primary_key.partition_key].split("#")[1]
        for item in response.items
    )
    historic_state_items: tuple[Item, ...] = tuple(
        chain.from_iterable(
            await collect(
                _get_historic_state_items(policy_id=policy_id)
                for policy_id in policies_ids
            )
        )
    )
    keys_to_delete = set(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response.items + historic_state_items
    )
    await operations.batch_delete_item(
        keys=tuple(keys_to_delete),
        table=TABLE,
    )
