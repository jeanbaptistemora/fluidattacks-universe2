# pylint: disable=invalid-name
"""
Search for removed findings in vms that belong to alive groups.
Look for both findings in DELETED status and those with keys modified with
preffix REMOVED#.

Store them in redshift if applies and remove them from vms.

Execution Time:     2022-02-10 at 22:15:34 UTC
Finalization Time:  2022-02-10 at 22:38:47 UTC
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from botocore.exceptions import (
    ClientError,
    HTTPClientError,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import db_model.findings as findings_model
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
    FindingVerification,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    dal as groups_dal,
)
import logging
import logging.config
from redshift.findings import (
    insert_batch_metadata,
    insert_batch_severity_cvss20,
    insert_batch_severity_cvss31,
    insert_batch_state,
    insert_batch_verification,
    insert_batch_verification_vuln_ids,
)
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


def filter_out_deleted_findings(
    *,
    findings: Tuple[Finding, ...],
) -> Tuple[Finding, ...]:
    return tuple(
        finding
        for finding in findings
        if "@fluid" not in finding.state.modified_by
        and "@kernelship" not in finding.state.modified_by
    )


async def send_findings_to_redshift(
    *,
    loaders: Dataloaders,
    findings: Tuple[Finding, ...],
) -> None:
    # Only deleted vulns by external users will be stored
    findings_to_store = filter_out_deleted_findings(findings=findings)
    if not findings_to_store:
        return

    findings_to_store_ids = [finding.id for finding in findings_to_store]
    state_loader = loaders.finding_historic_state
    verification_loader = loaders.finding_historic_verification
    findings_state: Tuple[
        Tuple[FindingState, ...], ...
    ] = await state_loader.load_many(findings_to_store_ids)
    findings_verification: Tuple[
        Tuple[FindingVerification, ...], ...
    ] = await verification_loader.load_many(findings_to_store_ids)

    await insert_batch_metadata(
        findings=findings_to_store,
    )
    await collect(
        (
            insert_batch_severity_cvss20(
                findings=findings_to_store,
            ),
            insert_batch_severity_cvss31(
                findings=findings_to_store,
            ),
            insert_batch_state(
                finding_ids=tuple(findings_to_store_ids),
                historics=findings_state,
            ),
            insert_batch_verification(
                finding_ids=tuple(findings_to_store_ids),
                historics=findings_verification,
            ),
            insert_batch_verification_vuln_ids(
                finding_ids=tuple(findings_to_store_ids),
                historics=findings_verification,
            ),
        )
    )


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        ClientPayloadError,
        CustomUnavailabilityError,
        HTTPClientError,
        ServerTimeoutError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    # Get findings with their current state status as DELETED
    group_drafts_and_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    findings_removed_status = tuple(
        finding
        for finding in group_drafts_and_findings
        if finding.state.status == FindingStateStatus.DELETED
    )
    # Get findings with their keys modified by REMOVED#
    findings_removed_preffix: Tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    target_findings = findings_removed_status + findings_removed_preffix

    if target_findings:
        await send_findings_to_redshift(
            loaders=loaders,
            findings=target_findings,
        )
        await collect(
            tuple(
                findings_model.remove(
                    group_name=group_name,
                    finding_id=finding.id,
                )
                for finding in target_findings
            ),
            workers=8,
        )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "removed": len(target_findings),
                "progress": str(progress),
            }
        },
    )


async def get_group_names() -> List[str]:
    return sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_alive_groups()
        ]
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    alive_groups = await get_group_names()
    alive_groups_len = len(alive_groups)
    LOGGER_CONSOLE.info(
        "Active and suspended groups",
        extra={
            "extra": {
                "alive_groups_len": alive_groups_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / alive_groups_len,
            )
            for count, group_name in enumerate(alive_groups)
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
