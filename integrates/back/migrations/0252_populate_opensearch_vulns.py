# pylint: disable=invalid-name
"""
Populates OpenSearch with all the vulns from active groups

Execution Time:    2022-08-09 at 13:59:41 UTC
Finalization Time: 2022-08-09 at 16:20:23 UTC
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
from opensearchpy.exceptions import (
    ConflictError,
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


async def process_vulnerability(vulnerability: dict[str, Any]) -> None:
    try:
        client = await get_client()
        await client.create(
            body=vulnerability,
            id="#".join([vulnerability["pk"], vulnerability["sk"]]),
            index="vulnerabilities",
        )
    except ConflictError:
        pass


async def process_finding(finding: Finding) -> None:
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
    vulnerabilities = response.items

    await collect(
        tuple(
            process_vulnerability(vulnerability)
            for vulnerability in vulnerabilities
        )
    )

    LOGGER.info(
        "Finding processed",
        extra={
            "extra": {
                "finding_id": finding.id,
                "vulnerabilities": len(vulnerabilities),
            }
        },
    )


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    group_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(process_finding(finding) for finding in group_findings)
    )


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    await search_startup()
    await collect(
        tuple(
            process_group(loaders, group_name)
            for group_name in active_group_names
        ),
        workers=5,
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
