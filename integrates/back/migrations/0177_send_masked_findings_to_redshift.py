# pylint: disable=invalid-name
"""
Search for findings in vms that belong to already removed groups.
These vulns were "masked" while redshift storage was not in place.

Store them in redshift if apply and remove them from vms.

Execution Time:
Finalization Time:
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
from boto3.dynamodb.conditions import (
    Attr,
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
        if finding.state.status != FindingStateStatus.DELETED
        or (
            finding.state.status == FindingStateStatus.DELETED
            and "@fluidattacks.com" not in finding.state.modified_by
        )
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
    group_drafts_and_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    group_removed_findings: Tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    all_findings = group_drafts_and_findings + group_removed_findings

    if not all_findings:
        return

    await send_findings_to_redshift(
        loaders=loaders,
        findings=all_findings,
    )
    await collect(
        tuple(
            findings_model.remove(
                group_name=group_name,
                finding_id=finding.id,
            )
            for finding in all_findings
        ),
        workers=64,
    )
    LOGGER_CONSOLE.info(
        "Group updated",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": str(progress),
            }
        },
    )


async def get_removed_groups() -> List[str]:
    filtering_exp = Attr("project_status").eq("DELETED") | Attr(
        "project_status"
    ).eq("FINISHED")
    return sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    removed_groups = await get_removed_groups()
    removed_groups_len = len(removed_groups)
    LOGGER_CONSOLE.info(
        "Removed groups",
        extra={
            "extra": {
                "removed_groups_len": removed_groups_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / removed_groups_len,
            )
            for count, group_name in enumerate(removed_groups)
        ),
        workers=32,
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
