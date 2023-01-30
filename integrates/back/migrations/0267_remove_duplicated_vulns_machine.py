# type: ignore

# pylint: disable=invalid-name
"""
This migration removes the duplicated vulnerabilities caused by a bug
in the batch action to move roots.

Execution Time: 2022-08-24T21:09:43+00:00
Finalization Time: 2022-08-24T23:40:21+00:00
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.remove import (
    remove,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import logging
from organizations.domain import (
    get_all_active_groups,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_hash_from_typed,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    findings = await loaders.group_findings.load(group_name)

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
        vulns: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in (
                await loaders.finding_vulnerabilities.load(finding.id)
            )
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.state.source == Source.MACHINE
        )
        vulns = tuple(
            sorted(
                vulns,
                key=lambda x: datetime.fromisoformat(
                    x.treatment.modified_date
                ).timestamp(),
            )
        )
        LOGGER_CONSOLE.info(
            "Vulns loaded",
            extra={
                "extra": {
                    "vulns": len(vulns),
                }
            },
        )
        unique_hashes = []
        duplicated: List[Vulnerability] = []

        for vuln in vulns:
            hash_identifier = get_hash_from_typed(vuln)
            if hash_identifier in unique_hashes:
                duplicated.append(vuln)
            else:
                unique_hashes.append(hash_identifier)

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
    loaders: Dataloaders = get_new_context()
    groups: List[str] = [
        group.name for group in await get_all_active_groups(loaders)
    ]  # Masked

    for group_name in reversed(groups):
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
