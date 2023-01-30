# pylint: disable=invalid-name
"""
Guarantee the states within the finding's historic state are
separated by at least one whole second.
This is required for analytics purposes.

Execution Time:    2022-10-05 at 21:47:13 UTC
Finalization Time: 2022-10-05 at 22:15:28 UTC
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
from db_model.utils import (
    adjust_historic_dates,
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


async def _process_finding(
    loaders: Dataloaders,
    finding_id: str,
    group_name: str,
) -> None:
    historic_state = await loaders.finding_historic_state.load(finding_id)
    adjusted_historic = adjust_historic_dates(historic_state)
    if historic_state != adjusted_historic:
        await findings_model.update_historic_state(
            group_name=group_name,
            finding_id=finding_id,
            historic_state=adjusted_historic,
        )
        LOGGER_CONSOLE.info(
            "Finding updated",
            extra={
                "extra": {
                    "finding_id": finding_id,
                    "group_name": group_name,
                }
            },
        )


async def _process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(
            _process_finding(
                loaders=loaders, finding_id=finding_id, group_name=group_name
            )
            for finding_id in [finding.id for finding in findings]
        ),
        workers=8,
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
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    active_group_names = sorted([group.name for group in active_groups])
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_group_names)}},
    )

    await collect(
        tuple(
            _process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(active_group_names),
            )
            for count, group_name in enumerate(active_group_names)
        ),
        workers=4,
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
