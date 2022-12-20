# type: ignore

# pylint: disable=invalid-name

"""
Populates OpenSearch with all the findings from active groups

Execution Time:    2022-12-20 at 18:16:25 UTC
Finalization Time: 2022-12-20 at 20:21:35 UTC
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


async def process_lines(lines: tuple[dict[str, Any], ...]) -> None:
    body = []

    for line in lines:
        action = {
            "index": {
                "_index": "toe_lines",
                "_id": "#".join([line["pk"], line["sk"]]),
            }
        }
        body.extend([action, line])

    client = await get_client()
    await client.bulk(body=body)


async def process_group(group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with("LINES#")
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
    )
    lines = response.items

    await collect(
        tuple(
            process_lines(lines_chunk) for lines_chunk in chunked(lines, 100)
        ),
        workers=2,
    )
    LOGGER.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "toe_lines": len(lines),
            }
        },
    )


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    await search_startup()
    client = await get_client()
    await client.indices.delete(index="toe_lines")
    await client.indices.create(index="toe_lines")
    await collect(
        tuple(process_group(group_name) for group_name in active_group_names),
        workers=2,
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
