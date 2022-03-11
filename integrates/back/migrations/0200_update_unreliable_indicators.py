# pylint: disable=invalid-name
"""
Update unreliable indicators for findings and vulns related to report_date.
An inconsistency is present due to a bug in the mutation approve_draft.

Execution Time:
Finalization Time:
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import groups.domain as groups_domain
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
from typing import (
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
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
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_all.load(finding.id)
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.unreliable_indicators.unreliable_report_date
        != await vulns_domain.get_report_date(loaders=loaders, vuln=vuln)
    ]

    if vulns_to_update:
        await update_unreliable_indicators_by_deps(
            EntityDependency.approve_draft,
            finding_ids=[],
            vulnerability_ids=[vuln.id for vuln in vulns_to_update],
        )

    finding_indicators = finding.unreliable_indicators
    if vulns_to_update or (
        finding.approval
        and finding_indicators.unreliable_newest_vulnerability_report_date
        < finding.approval.modified_date
    ):
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding.id],
            vulnerability_ids=[],
        )


async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    await collect(
        tuple(
            process_finding(
                loaders=loaders,
                finding=finding,
            )
            for finding in findings
        ),
        workers=4,
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
