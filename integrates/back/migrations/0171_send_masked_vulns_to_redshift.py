# pylint: disable=invalid-name
"""
Search for vulns in vms that belong to already removed groups. This vulns
were "masked" while redshift storage was not in place.

Store them in redshift and remove them from vms.

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
from boto3.dynamodb.conditions import (
    Attr,
)
from botocore.exceptions import (
    HTTPClientError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
import db_model.vulnerabilities as vulns_model
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from decorators import (
    retry_on_exceptions,
)
from groups import (
    dal as groups_dal,
)
import logging
import logging.config
from redshift.vulnerabilities import (
    insert_batch_metadata,
    insert_batch_state,
    insert_batch_treatment,
    insert_batch_verification,
    insert_batch_zero_risk,
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

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def filter_out_deleted_vulns(
    *,
    vulns: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulns
        if vuln.state.status != VulnerabilityStateStatus.DELETED
        or (
            vuln.state.status == VulnerabilityStateStatus.DELETED
            and "@fluidattacks.com" not in vuln.state.modified_by
        )
    )


async def send_vulns_to_redshift(
    *,
    loaders: Dataloaders,
    finding: Finding,
    vulns: Tuple[Vulnerability, ...],
) -> None:
    if finding.state.status not in {
        FindingStateStatus.APPROVED,
        FindingStateStatus.DELETED,
    }:
        # Only vulns for released findings will be stored
        return

    # Only deleted vulns by external users will be stored
    vulns_to_store = filter_out_deleted_vulns(vulns=vulns)
    if not vulns_to_store:
        return

    vulns_to_store_id = [vuln.id for vuln in vulns_to_store]
    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    vulns_state: Tuple[
        Tuple[VulnerabilityState, ...], ...
    ] = await state_loader.load_many(vulns_to_store_id)
    vulns_treatment: Tuple[
        Tuple[VulnerabilityTreatment, ...], ...
    ] = await treatment_loader.load_many(vulns_to_store_id)
    vulns_verification: Tuple[
        Tuple[VulnerabilityVerification, ...], ...
    ] = await verification_loader.load_many(vulns_to_store_id)
    vulns_zero_risk: Tuple[
        Tuple[VulnerabilityZeroRisk, ...], ...
    ] = await zero_risk_loader.load_many(vulns_to_store_id)

    await insert_batch_metadata(
        vulnerabilities=vulns_to_store,
    )
    await insert_batch_state(
        vulnerability_ids=tuple(vulns_to_store_id),
        historics=vulns_state,
    )
    await insert_batch_treatment(
        vulnerability_ids=tuple(vulns_to_store_id),
        historics=vulns_treatment,
    )
    await insert_batch_verification(
        vulnerability_ids=tuple(vulns_to_store_id),
        historics=vulns_verification,
    )
    await insert_batch_zero_risk(
        vulnerability_ids=tuple(vulns_to_store_id),
        historics=vulns_zero_risk,
    )


async def process_finding(
    *,
    loaders: Dataloaders,
    finding: Finding,
) -> None:
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_all_typed.load(finding.id)

    if not vulns:
        return

    await send_vulns_to_redshift(
        loaders=loaders,
        finding=finding,
        vulns=vulns,
    )
    await collect(
        tuple(vulns_model.remove(vulnerability_id=vuln.id) for vuln in vulns),
        workers=8,
    )


@retry_on_exceptions(
    exceptions=(
        HTTPClientError,
        ClientConnectorError,
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
    await collect(
        tuple(
            process_finding(loaders=loaders, finding=finding)
            for finding in all_findings
        ),
        workers=8,
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
        workers=8,
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
