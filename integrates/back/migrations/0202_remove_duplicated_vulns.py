# pylint: disable=invalid-name
"""
This migration removes the duplicated vulnerabilities caused by a bug
in the batch action to move roots.

Execution Time:    2022-04-06 at 19:06:34 UTC-5
Finalization Time: 2022-04-07 at 03:07:26 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.remove import (
    remove,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import logging
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
    Tuple,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )

    for index, finding in enumerate(findings):
        LOGGER_CONSOLE.info(
            "Processing finding",
            extra={
                "extra": {
                    "finding_id": finding.id,
                    "progress": f"{index + 1}/{len(findings)}",
                }
            },
        )
        vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(finding.id)
        LOGGER_CONSOLE.info(
            "Vulns loaded",
            extra={
                "extra": {
                    "vulns": len(vulns),
                }
            },
        )
        unique = []
        duplicated: List[Vulnerability] = []

        for vuln in vulns:
            unique_identifiers = (vuln.where, vuln.specific, vuln.root_id)
            if unique_identifiers in unique:
                duplicated.append(vuln)
            else:
                unique.append(unique_identifiers)

        LOGGER_CONSOLE.info(
            "Will remove",
            extra={
                "extra": {
                    "finding_id": finding.id,
                    "duplicated": len(duplicated),
                }
            },
        )
        await collect(
            tuple(remove(vulnerability_id=vuln.id) for vuln in duplicated),
            workers=1024,
        )
        LOGGER_CONSOLE.info(
            "Finding processed",
            extra={
                "extra": {
                    "finding_id": finding.id,
                    "duplicated": len(duplicated),
                }
            },
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
    groups: List[str] = []  # Masked
    loaders: Dataloaders = get_new_context()

    for group_name in groups:
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
