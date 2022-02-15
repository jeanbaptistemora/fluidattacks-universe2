# pylint: disable=invalid-name
"""
Populate in redshift missing field "modified_by" from vuln state.
Info is restored from old table "FI_vulnerabilities".
Based on migration 0172, check it out.

Execution Time:     2022-02-01 at 18:36:43 UTC
Finalization Time:  2022-02-01 at 23:45:45 UTC
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
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from db_model.vulnerabilities.utils import (
    adjust_historic_dates,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from dynamodb.types import (
    Item,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
import logging
import logging.config
from newutils.vulnerabilities import (
    format_vulnerability_state,
)
from redshift import (
    operations as redshift_ops,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
from vulnerabilities import (
    dal as vulns_dal,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _update_state_redshift(
    *,
    vulns_id: Tuple[Vulnerability, ...],
    vulns_state: Tuple[Tuple[VulnerabilityState, ...], ...],
) -> None:
    sql_vars = [
        dict(
            id=vuln_id,
            modified_by=state.modified_by,
            modified_date=state.modified_date,
        )
        for vuln_id, historic_state in zip(vulns_id, vulns_state)
        for state in historic_state
    ]
    await redshift_ops.execute_batch(  # nosec
        sql_query="""
            UPDATE integrates.vulnerabilities_state
            SET modified_by=%(modified_by)s
            WHERE id=%(id)s and modified_date=%(modified_date)s
        """,
        sql_vars=sql_vars,
    )


def _check_vuln_item_state(vuln: Item) -> bool:
    last_state: Dict[str, Any] = vuln["historic_state"][-1]
    state_status = str(last_state["state"]).upper()
    if state_status != "DELETED":
        return True

    modified_by = last_state.get("analyst") or last_state.get("hacker") or ""
    if (
        state_status == "DELETED"
        and "@fluid" not in modified_by
        and "@kernelship" not in modified_by
    ):
        return True

    return False


def _filter_out_deleted_vulns(
    vulns: List[Item],
) -> List[Item]:
    return [vuln for vuln in vulns if _check_vuln_item_state(vuln)]


async def _get_vulnerabilities_by_finding(finding_id: str) -> List[Item]:
    items: List[Item] = await vulns_dal.get_by_finding(finding_id=finding_id)
    return items


def _format_state(
    vulns_items: List[Item],
) -> Tuple[Tuple[VulnerabilityState, ...], ...]:
    return tuple(
        adjust_historic_dates(
            tuple(
                format_vulnerability_state(state)
                for state in vulnerability["historic_state"]
            )
        )
        for vulnerability in vulns_items
    )


@retry_on_exceptions(
    exceptions=(
        ClientError,
        ClientPayloadError,
        CustomUnavailabilityError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_finding(
    *,
    finding: Finding,
) -> List[Item]:
    # Only vulns for released findings will be stored
    if finding.state.status not in {
        FindingStateStatus.APPROVED,
        FindingStateStatus.DELETED,
    }:
        return []

    # Retrieve vulns as dict from old table
    vulns_items = await _get_vulnerabilities_by_finding(finding_id=finding.id)
    if not vulns_items:
        return []

    # Only deleted vulns by external users will be stored
    vulns_items_to_store = _filter_out_deleted_vulns(vulns_items)
    if not vulns_items_to_store:
        return []

    return vulns_items_to_store


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
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
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    group_removed_findings: Tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    all_findings = group_findings + group_removed_findings
    vulns_items_to_store: List[Item] = list(
        chain.from_iterable(
            await collect(
                tuple(
                    process_finding(finding=finding)
                    for finding in all_findings
                ),
                workers=64,
            )
        )
    )
    vulns_id = tuple(vuln["UUID"] for vuln in vulns_items_to_store)
    vulns_state = _format_state(vulns_items_to_store)
    await _update_state_redshift(
        vulns_id=vulns_id,
        vulns_state=vulns_state,
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
