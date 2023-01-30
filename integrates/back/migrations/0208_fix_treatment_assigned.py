# pylint: disable=invalid-name
"""
Update vuln treatment assigned index for all vulns.
The related vms index is gsi_3.

Execution Time:     2022-04-28 at 23:06:39 UTC
Finalization Time:  2022-04-28 at 23:12:09 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.update import (
    update_assigned_index,
)
from db_model.vulnerabilities.utils import (
    format_state,
    format_treatment,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
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


async def process_vuln(
    finding_id: str,
    item: Item,
) -> None:
    state = format_state(item["state"])
    if state.status != VulnerabilityStateStatus.VULNERABLE:
        return

    treatment = (
        format_treatment(item["treatment"]) if "treatment" in item else None
    )
    if not treatment or not treatment.assigned:
        return

    if (
        treatment.status == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
    ):
        return

    user_pk_3 = (
        str(item["pk_3"]).split("#")[1] if item["pk_3"] != "USER" else ""
    )
    if user_pk_3 != treatment.assigned:
        vuln_id = str(item["pk"]).split("#")[1]
        await update_assigned_index(
            finding_id=finding_id,
            entry=treatment,
            vulnerability_id=vuln_id,
        )


async def get_finding_vulns(
    finding_id: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def process_finding(
    finding_id: str,
) -> None:
    vuln_items = await get_finding_vulns(finding_id)
    await collect(
        tuple(process_vuln(finding_id, item) for item in vuln_items),
        workers=8,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_findings.load(group_name)
    await collect(
        tuple(
            process_finding(finding_id)
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
            process_group(
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
