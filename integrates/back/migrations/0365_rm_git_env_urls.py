# pylint: disable=invalid-name
"""
Remove git_environment_urls from root state
"""
from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import logging
import logging.config
from organizations.domain import (
    get_all_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_historic_state(*, root_id: str) -> list[dict]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_historic_state"],
        ),
        table=TABLE,
    )

    return list(response.items)


async def _get_group_roots(*, group_name: str) -> list[dict]:
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

    return list(response.items)


async def _process_historic_root_state(
    *,
    root_id: str,
    state: dict,
) -> None:
    key_structure = TABLE.primary_key
    historic_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={
            "uuid": root_id,
            "iso8601utc": state["sk"].split("#")[1],
        },
    )

    if state["git_environment_urls"] != []:
        LOGGER_CONSOLE.info(
            "non empty git_environment_urls historic state",
            extra=dict(
                extra=dict(
                    partition_key=historic_key.partition_key,
                    sort_key=historic_key.sort_key,
                    state=state,
                )
            ),
        )
        return

    item = {"git_environment_urls": None}
    LOGGER_CONSOLE.info(
        "historic have to update",
        extra=dict(
            extra=dict(
                partition_key=historic_key.partition_key,
                sort_key=historic_key.sort_key,
            )
        ),
    )
    with suppress(ConditionalCheckFailedException):
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists()
            & Attr(key_structure.sort_key).eq(historic_key.sort_key),
            item=item,
            key=historic_key,
            table=TABLE,
        )
        return
    LOGGER_CONSOLE.info(
        "historic exception",
        extra=dict(
            extra=dict(
                partition_key=historic_key.partition_key,
                sort_key=historic_key.sort_key,
            )
        ),
    )


async def _process_root_state(
    *,
    group_name: str,
    root_id: str,
    state: dict,
) -> None:
    key_structure = TABLE.primary_key
    root_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
    )

    if state["git_environment_urls"] != []:
        LOGGER_CONSOLE.info(
            "non empty git_environment_urls state",
            extra=dict(
                extra=dict(
                    partition_key=root_key.partition_key,
                    sort_key=root_key.sort_key,
                    state=state,
                )
            ),
        )
        return

    root_item = {"state.git_environment_urls": None}
    LOGGER_CONSOLE.info(
        "state have to update",
        extra=dict(
            extra=dict(
                partition_key=root_key.partition_key,
                sort_key=root_key.sort_key,
            )
        ),
    )
    with suppress(ConditionalCheckFailedException):
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=root_item,
            key=root_key,
            table=TABLE,
        )
        return
    LOGGER_CONSOLE.info(
        "state exception",
        extra=dict(extra=dict(partition_key=root_key.partition_key)),
    )


async def process_group(group_name: str) -> None:
    group_roots = await _get_group_roots(group_name=group_name)

    for root in group_roots:
        if "git_environment_urls" in root["state"]:
            await _process_root_state(
                group_name=group_name,
                root_id=root["pk"].split("#")[1],
                state=root["state"],
            )
        else:
            LOGGER_CONSOLE.info(
                "state not to have to update",
                extra=dict(
                    extra=dict(
                        partition_key=root["pk"].split("#")[1],
                        state=root["state"],
                    )
                ),
            )

        historic_states = await _get_historic_state(
            root_id=root["pk"].split("#")[1]
        )
        for state in historic_states:
            if "git_environment_urls" in state:
                await _process_historic_root_state(
                    root_id=root["pk"].split("#")[1], state=state
                )
            else:
                LOGGER_CONSOLE.info(
                    "historic not to have to update",
                    extra=dict(
                        extra=dict(
                            partition_key=root["pk"].split("#")[1], state=state
                        )
                    ),
                )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(await get_all_group_names(loaders=loaders))
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
