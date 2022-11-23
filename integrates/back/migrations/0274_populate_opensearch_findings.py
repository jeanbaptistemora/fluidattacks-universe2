# type: ignore

# pylint: disable=invalid-name
"""
Populates OpenSearch with all the findings from active groups

Execution Time:    2022-09-09 at 21:04:22 UTC
Finalization Time: 2022-09-09 at 21:06:57 UTC
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


async def process_findings(findings: tuple[dict[str, Any], ...]) -> None:
    body = []

    for finding in findings:
        action = {
            "index": {
                "_index": "findings",
                "_id": "#".join([finding["pk"], finding["sk"]]),
            }
        }
        body.extend([action, finding])

    client = await get_client()
    await client.bulk(body=body)


async def process_group(group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
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
        facets=(TABLE.facets["finding_metadata"],),
        index=index,
        table=TABLE,
    )
    findings = response.items

    await collect(
        tuple(
            process_findings(findings_chunk)
            for findings_chunk in chunked(findings, 100)
        )
    )
    LOGGER.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "findings": len(findings),
            }
        },
    )


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    await search_startup()
    client = await get_client()
    await client.indices.delete(index="findings")
    await client.indices.create(index="findings")
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
