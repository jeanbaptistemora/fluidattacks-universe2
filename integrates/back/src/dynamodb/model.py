from boto3.dynamodb.conditions import (
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
    tables,
)
from dynamodb.types import (
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

with open(FI_DB_MODEL_PATH, mode="r", encoding="utf-8") as file:
    TABLE = tables.load_tables(json.load(file))[0]


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
    response = await operations.query(
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

    if response.items:
        return _build_org_policy_finding(
            org_name=org_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=response.items,
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
    response = await operations.query(
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
    for item in response.items:
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

    await operations.batch_put_item(items=items, table=TABLE)


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

    await operations.batch_put_item(items=historic, table=TABLE)
