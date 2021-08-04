from boto3.dynamodb.conditions import (
    Key,
)
from collections import (
    defaultdict,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    build_root,
)
from dynamodb.types import (
    RootItem,
)
from typing import (
    Optional,
    Tuple,
)


async def get_root(
    *,
    group_name: str,
    root_id: str,
) -> Optional[RootItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
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
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return build_root(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    return None


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
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
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    root_items = defaultdict(list)
    for item in results:
        root_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        root_items[root_id].append(item)

    return tuple(
        build_root(
            group_name=group_name,
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for root_id, items in root_items.items()
    )
