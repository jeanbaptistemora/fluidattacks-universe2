# pylint: disable=invalid-name
"""
Remove the where, specific and and commit from the vulnerability since it is
stored in the vulnerability state

Execution Time:    2022-11-08 at 21:28:54 UTC
Finalization Time: 2022-11-08 at 22:31:20 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from botocore.exceptions import (
    ConnectTimeoutError,
    ReadTimeoutError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
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


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def process_vulnerability(vulnerability: Vulnerability) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    key_structure = TABLE.primary_key
    item = {
        "commit": None,
        "specific": None,
        "where": None,
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def get_finding_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
) -> tuple[Vulnerability, ...]:
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    return vulnerabilities  # type: ignore


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    findings = await loaders.group_drafts_and_findings.load(group_name)
    vulnerabilities = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_finding_vulnerabilities(loaders, finding.id)
                    for finding in findings
                ),
                workers=500,
            )
        )
    )
    await collect(
        tuple(
            process_vulnerability(vulnerability)
            for vulnerability in vulnerabilities
        ),
        workers=500,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "all_vulnerabilities": len(vulnerabilities),
            }
        },
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names = sorted(
        tuple(
            chain.from_iterable(
                await collect(
                    tuple(
                        orgs_domain.get_group_names(loaders, organization_id)
                        for organization_id in all_organization_ids
                    ),
                    workers=100,
                )
            )
        )
    )
    count = 0
    print("all_group_names", len(all_group_names))
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
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
