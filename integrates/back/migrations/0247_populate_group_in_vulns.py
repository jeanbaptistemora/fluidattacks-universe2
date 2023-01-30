# pylint: disable=invalid-name
"""
Sets to group_name attribute to all vulnerabilities

Execution Time:    2022-07-25 at 20:14:23 UTC
Finalization Time: 2022-07-25 at 20:52:55 UTC

Execution Time:    2022-07-26 at 13:46:09 UTC
Finalization Time: 2022-07-26 at 13:50:16 UTC
"""


from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def process_vulnerability(
    group_name: str, vulnerability: Vulnerability
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item={"group_name": group_name},
        key=vulnerability_key,
        table=TABLE,
    )


async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding.id
    )

    await collect(
        tuple(
            process_vulnerability(finding.group_name, vulnerability)
            for vulnerability in vulnerabilities
            if not vulnerability.group_name
        ),
        workers=100,
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


async def main() -> None:
    loaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    total = len(active_group_names)

    for count, group_name in enumerate(active_group_names):
        LOGGER.info(
            "Processing group",
            extra={
                "extra": {
                    "group_name": group_name,
                    "progress": f"{count + 1}/{total}",
                }
            },
        )
        group_findings = await loaders.group_drafts_and_findings.load(
            group_name
        )
        await collect(
            tuple(
                process_finding(loaders, finding) for finding in group_findings
            )
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
