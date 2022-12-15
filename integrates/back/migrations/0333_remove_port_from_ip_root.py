# pylint: disable=invalid-name
"""
Remove port from ip root

Execution Time:    2022-12-15 at 23:07:38 UTC
Finalization Time: 2022-12-15 at 23:10:51 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_historic_state(*, root_id: str) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["ip_root_historic_state"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["ip_root_historic_state"],),
        table=TABLE,
    )

    return response.items


async def process_root(root: Item) -> None:
    root_key = PrimaryKey(
        partition_key=root["pk"],
        sort_key=root["sk"],
    )
    condition_expression = Attr(TABLE.primary_key.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        key=root_key,
        item={
            "state.port": None,
        },
        table=TABLE,
    )
    root_id = root["pk"].split("#")[1]
    historic_state = await _get_historic_state(root_id=root_id)
    await collect(
        tuple(
            operations.update_item(
                condition_expression=condition_expression,
                key=PrimaryKey(
                    partition_key=state["pk"],
                    sort_key=state["sk"],
                ),
                item={
                    "port": None,
                },
                table=TABLE,
            )
            for state in historic_state
        )
    )


async def _get_group_roots(*, group_name: str) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
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
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        index=index,
        table=TABLE,
    )
    return response.items


async def process_group(
    group_name: str,
) -> None:
    ip_roots = [
        root
        for root in await _get_group_roots(group_name=group_name)
        if root["type"] == "IP"
    ]
    await collect(
        tuple(process_root(root) for root in ip_roots),
    )


async def main() -> None:
    loaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_active_group_names(loaders)
    )
    count = 0
    LOGGER_CONSOLE.info(
        "All group names",
        extra={
            "extra": {
                "total": len(all_group_names),
            }
        },
    )
    for group_name in all_group_names:
        count += 1
        LOGGER_CONSOLE.info(
            "Group",
            extra={
                "extra": {
                    "group_name": group_name,
                    "count": count,
                }
            },
        )
        await process_group(group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
