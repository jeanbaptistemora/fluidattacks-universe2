# pylint: disable=invalid-name
"""
Populate the finding unfulfilled requirements with the criteria files

Execution Time:    2023-02-17 at 20:49:19 UTC
Finalization Time: 2023-02-17 at 20:56:24 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingMetadataToUpdate,
)
import logging
import logging.config
from newutils.findings import (
    get_vulns_file,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_finding(
    finding: Finding, vulnerabilities_file: dict[str, Any]
) -> None:
    criteria_vulnerability_id = finding.title.split(".")[0].strip()
    criteria_vulnerability = vulnerabilities_file.get(
        criteria_vulnerability_id
    )
    requirements: list[str] = (
        criteria_vulnerability["requirements"]
        if criteria_vulnerability
        else []
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=FindingMetadataToUpdate(
            unfulfilled_requirements=requirements
        ),
    )


async def process_group(
    group_name: str, vulnerabilities_file: dict[str, Any]
) -> None:
    loaders: Dataloaders = get_new_context()
    findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(
            process_finding(finding, vulnerabilities_file)
            for finding in findings
        )
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
    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    vulnerabilities_file = await get_vulns_file()
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
        await process_group(group_name, vulnerabilities_file)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
