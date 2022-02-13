# pylint: disable=invalid-name
"""
This migration merges metadata, state and cloning into the same item,
which translates to faster queries due to less returned items and enables
get item operations that allow developers to load roots in an efficient way.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from collections import (
    defaultdict,
)
from contextlib import (
    suppress,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    historics,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
import logging
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


index = TABLE.indexes["inverted_index"]
key_structure = index.primary_key


async def process_root(root_id: str, items: List[Dict[str, Any]]) -> None:
    metadata = historics.get_metadata(
        item_id=root_id, key_structure=key_structure, raw_items=items
    )
    state = historics.get_latest(
        item_id=root_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=items,
    )
    root_key = PrimaryKey(
        partition_key=metadata["pk"], sort_key=metadata["sk"]
    )

    if metadata.get("state") is None:
        with suppress(ConditionalCheckFailedException):
            await operations.update_item(
                condition_expression=(Attr("state").not_exists()),
                item={"state": state},
                key=root_key,
                table=TABLE,
            )

    if metadata["type"] == "Git" and metadata.get("cloning") is None:
        cloning = historics.get_latest(
            item_id=root_id,
            key_structure=key_structure,
            historic_suffix="CLON",
            raw_items=items,
        )
        with suppress(ConditionalCheckFailedException):
            await operations.update_item(
                condition_expression=(Attr("cloning").not_exists()),
                item={"cloning": cloning},
                key=root_key,
                table=TABLE,
            )


async def process_group(group_name: str, progress: float) -> None:
    response = await operations.query(
        condition_expression=(
            Key("sk").eq(f"GROUP#{group_name}")
            & Key("pk").begins_with("ROOT#")
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
    for item in response.items:
        root_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        root_items[root_id].append(item)

    await collect(
        tuple(
            process_root(root_id, items)
            for root_id, items in root_items.items()
        ),
        workers=10,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "roots": len(root_items),
                "progress": str(progress),
            }
        },
    )


async def get_group_names() -> List[str]:
    return sorted(
        group["project_name"] for group in await groups_dal.get_alive_groups()
    )


async def main() -> None:
    alive_groups = await get_group_names()

    await collect(
        tuple(
            process_group(group_name, count / len(alive_groups))
            for count, group_name in enumerate(alive_groups)
        ),
        workers=10,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
