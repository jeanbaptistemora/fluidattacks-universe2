# type: ignore

# pylint: disable=invalid-name
"""
Populate unreliable_is_verification_summary for all findings with the right
value.

Execution Time:    2022-05-11 at 14:14:51 UTC
Finalization Time: 2022-05-11 at 14:22:00 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import logging
import logging.config
from organizations.domain import (
    iterate_organizations_groups,
)
from settings import (
    LOGGING,
)
import time
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(
        CustomUnavailabilityError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_finding(
    *,
    finding: Finding,
) -> None:
    #  request_vulnerabilities_hold is dependency of is_verification_summary
    await update_unreliable_indicators_by_deps(
        EntityDependency.request_vulnerabilities_hold,
        finding_ids=[finding.id],
        vulnerability_ids=[],
    )


async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(
            process_finding(
                finding=finding,
            )
            for finding in findings
        ),
        workers=100,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = []
    async for _, _, org_group_names in iterate_organizations_groups():
        group_names.extend(org_group_names)
    group_names_len = len(group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "group_names_len": group_names_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(set(group_names))
        ),
        workers=3,
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
