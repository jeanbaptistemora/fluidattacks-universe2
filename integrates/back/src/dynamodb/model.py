from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from collections import (
    defaultdict,
)
from context import (
    FI_DB_MODEL_PATH,
)
from dynamodb import (
    historics,
    keys,
    operations,
    table,
)
from dynamodb.types import (
    GroupMetadata,
    Item,
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
    PrimaryKey,
)
import json
from typing import (
    Optional,
    Tuple,
)

with open(FI_DB_MODEL_PATH, mode="r") as file:
    TABLE = table.load_tables(json.load(file))[0]


def _build_org_policy_finding(
    *,
    org_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> OrgFindingPolicyItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    return OrgFindingPolicyItem(
        id=metadata[key_structure.sort_key].split("#")[1],
        org_name=org_name,
        metadata=OrgFindingPolicyMetadata(
            name=metadata["name"], tags=metadata.get("tags", {})
        ),
        state=OrgFindingPolicyState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            status=state["status"],
        ),
    )


async def get_org_finding_policy(
    *,
    org_name: str,
    finding_policy_id: str,
) -> Optional[OrgFindingPolicyItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name, "uuid": finding_policy_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["org_finding_policy_metadata"],
            TABLE.facets["org_finding_policy_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return _build_org_policy_finding(
            org_name=org_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    return None


async def get_org_finding_policies(
    *, org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["org_finding_policy_metadata"],
            TABLE.facets["org_finding_policy_state"],
        ),
        index=index,
        table=TABLE,
    )

    org_findings_policies_items = defaultdict(list)
    for item in results:
        finding_policy_id = "#".join(
            item[key_structure.sort_key].split("#")[:2]
        )
        org_findings_policies_items[finding_policy_id].append(item)

    return tuple(
        _build_org_policy_finding(
            org_name=org_name,
            item_id=finding_policy_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for finding_policy_id, items in org_findings_policies_items.items()
    )


async def add_organization_finding_policy(
    *, finding_policy: OrgFindingPolicyItem
) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": finding_policy.org_name, "uuid": finding_policy.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(finding_policy.metadata._asdict()),
    }

    historic_state = historics.build_historic(
        attributes=dict(finding_policy.state._asdict()),
        historic_facet=TABLE.facets["org_finding_policy_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": finding_policy.state.modified_date,
            "name": finding_policy.org_name,
            "uuid": finding_policy.id,
        },
        latest_facet=TABLE.facets["org_finding_policy_state"],
    )
    items = (initial_metadata, *historic_state)

    await operations.batch_write_item(items=items, table=TABLE)


async def update_organization_finding_policy_state(
    *, org_name: str, finding_policy_id: str, state: OrgFindingPolicyState
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets["org_finding_policy_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": org_name,
            "uuid": finding_policy_id,
        },
        latest_facet=TABLE.facets["org_finding_policy_state"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def create_group_metadata(*, group_metadata: GroupMetadata) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["group_metadata"]
    metadata_key = keys.build_key(
        facet=facet, values={"name": group_metadata.name}
    )
    metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(group_metadata._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=metadata,
        table=TABLE,
    )


async def update_group_agent_token(
    *,
    group_name: str,
    agent_token: str,
) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )
    item = {"agent_token": agent_token}
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=item,
        key=key,
        table=TABLE,
    )


async def get_agent_token(*, group_name: str) -> Optional[str]:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        table=TABLE,
    )
    if results:
        return results[0]["agent_token"]

    return None
