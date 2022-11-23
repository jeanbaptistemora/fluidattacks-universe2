# type: ignore

# pylint: disable=invalid-name

"""
Populates OpenSearch with all the findings from active groups

Execution Time:    2022-09-27 at 01:40:20 UTC
Finalization Time: 2022-09-27 at 01:42:56 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
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
import logging
import logging.config
from more_itertools import (
    chunked,
)
from organizations.domain import (
    get_all_active_group_names,
)
from search.client import (
    get_client,
    search_shutdown,
    search_startup,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def process_executions(executions: tuple[dict[str, Any], ...]) -> None:
    body = []

    for execution in executions:
        action = {
            "index": {
                "_index": "forces_executions",
                "_id": "#".join([execution["pk"], execution["sk"]]),
            }
        }
        body.extend([action, execution])

    client = await get_client()
    await client.bulk(body=body)


async def process_group(group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["forces_execution"],
        values={"name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.sort_key).eq(
        primary_key.sort_key
    ) & Key(key_structure.partition_key).begins_with(primary_key.partition_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["forces_execution"],),
        table=TABLE,
        index=index,
    )
    executions = response.items

    await collect(
        tuple(
            process_executions(executions_chunk)
            for executions_chunk in chunked(executions, 100)
        )
    )
    LOGGER.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "executions": len(executions),
            }
        },
    )


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    await search_startup()
    client = await get_client()
    await client.indices.delete(index="forces_executions")
    await client.indices.create(index="forces_executions")
    await collect(
        tuple(process_group(group_name) for group_name in active_group_names),
        workers=4,
    )
    await search_shutdown()


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
