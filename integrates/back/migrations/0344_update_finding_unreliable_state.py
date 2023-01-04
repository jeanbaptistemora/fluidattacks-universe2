# pylint: disable=invalid-name
"""
update unreliable state for all the findings
Execution Time:    2023-01-04 at 05:02:20 UTC
Finalization Time: 2023-01-04 at 05:44:31 UTC
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
from db_model.organizations.get import (
    iterate_organizations,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_finding_unreliable_indicators,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)

    await collect(
        tuple(
            update_finding_unreliable_indicators(
                finding.id,
                {EntityAttr.status},
            )
            for finding in findings
        ),
        workers=8,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "all_findings": len(findings),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    count = 0
    groups = []
    async for organization in iterate_organizations():
        org_groups = await loaders.organization_groups.load(organization.id)
        groups.extend(org_groups)
    for group in groups:
        count += 1
        LOGGER_CONSOLE.info(
            "Group",
            extra={
                "extra": {
                    "group_name": group.name,
                    "count": count,
                }
            },
        )
        await process_group(group.name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
