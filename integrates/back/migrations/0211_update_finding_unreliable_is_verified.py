# type: ignore

# pylint: disable=invalid-name
"""
Update unreliable_is_verified for all findings with the right value.

Execution Time: 2022-04-29 at 19:55:42 UTC
Finalization Time: 2022-04-29 at 19:59:54 UTC
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
from findings import (
    domain as findings_domain,
)
import groups.domain as groups_domain
import logging
import logging.config
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
    loaders: Dataloaders,
    finding: Finding,
) -> None:
    is_verified = await findings_domain.get_is_verified(loaders, finding.id)
    if is_verified != finding.unreliable_indicators.unreliable_is_verified:
        # request_vulnerabilities_hold is dependency of finding is_verified
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
    findings = await loaders.group_findings.load(group_name)
    await collect(
        tuple(
            process_finding(
                loaders=loaders,
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
    group_names = sorted(await groups_domain.get_active_groups())
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
            for count, group_name in enumerate(group_names)
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
