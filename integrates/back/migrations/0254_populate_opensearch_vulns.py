# type: ignore

# pylint: disable=invalid-name
"""
Populates OpenSearch with all the vulns from active groups

Execution Time:    2022-08-09 at 13:59:41 UTC
Finalization Time: 2022-08-09 at 16:20:23 UTC

Execution Time:    2022-08-10 at 13:18:44 UTC
Finalization Time: 2022-08-10 at 13:37:27 UTC

Execution Time:    2022-11-03 at 23:28:48 UTC
Finalization Time: 2022-11-03 at 23:44:21 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from opensearchpy._async.helpers import (
    async_bulk,
)
from opensearchpy.helpers import (
    BulkIndexError,
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


def _format_vulnerability(vulnerability: dict[str, Any]) -> dict[str, Any]:
    # Needed as it doesn't fit in OpenSearch long data type (2^63)
    if "hash" in vulnerability:
        return {**vulnerability, "hash": str(vulnerability["hash"])}
    return vulnerability


async def process_vulnerabilities(
    group_name: str, vulnerabilities: tuple[dict[str, Any], ...]
) -> None:
    actions = [
        {
            "_id": "#".join([vulnerability["pk"], vulnerability["sk"]]),
            "_index": "vulnerabilities",
            "_op_type": "index",
            "_source": _format_vulnerability(vulnerability),
        }
        for vulnerability in vulnerabilities
    ]
    client = await get_client()
    try:
        await async_bulk(client=client, actions=actions)
    except BulkIndexError as ex:
        for error in ex.errors:
            print(group_name, error["index"]["error"]["reason"])


async def get_vulns(finding: Finding) -> tuple[dict[str, Any]]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding.id},
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
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )
    return response.items


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    group_findings = await loaders.group_drafts_and_findings.load(group_name)
    vulnerabilities = [
        vuln
        for finding_vulns in await collect(
            tuple(get_vulns(finding) for finding in group_findings),
        )
        for vuln in finding_vulns
    ]
    await process_vulnerabilities(group_name, vulnerabilities)

    LOGGER.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "vulnerabilities": len(vulnerabilities),
            }
        },
    )


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    await search_startup()
    client = await get_client()
    await client.indices.delete(index="vulnerabilities")
    await client.indices.create(index="vulnerabilities")
    try:
        await collect(
            tuple(
                process_group(loaders, group_name)
                for group_name in active_group_names
            ),
            workers=5,
        )
    finally:
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
