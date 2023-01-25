# type: ignore

# pylint: disable=invalid-name,unexpected-keyword-arg
"""
This migration removes the duplicated vulnerabilities caused by a bug
in the batch action to move roots.

Execution Time:
Finalization Time:
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
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
from organizations.domain import (
    get_all_active_groups,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
    Tuple,
)
from vulnerabilities.domain.core import (
    remove_vulnerability,
)
from vulnerabilities.domain.utils import (
    get_hash_from_typed,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def remove_state(*, vulnerability_id: str, date: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={"id": vulnerability_id, "iso8601utc": date},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_state"],),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )


async def process_group(  # pylint: disable=too-many-locals
    loaders: Dataloaders,
    group_name: str,
) -> None:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )

    for finding in findings:
        vulns = await loaders.finding_vulnerabilities.load(finding.id)
        vulns = tuple(
            vuln for vuln in vulns if vuln.state.source == Source.MACHINE
        )

        vulns = tuple(
            sorted(
                vulns,
                key=lambda x: datetime.fromisoformat(
                    x.treatment.modified_date
                ).timestamp(),
            )
        )

        unique_hashes = []
        duplicated_hashes = []
        unique_vulns: List[Vulnerability] = []
        duplicated: List[Vulnerability] = []

        for vuln in vulns:
            hash_identifier = get_hash_from_typed(vuln)
            if hash_identifier in unique_hashes:
                duplicated.append(vuln)
                duplicated_hashes.append(hash_identifier)
            else:
                unique_hashes.append(hash_identifier)
                unique_vulns.append(vuln)
        unique_ids = [vuln.id for vuln in unique_vulns]
        open_duplicates = [
            vuln
            for vuln in vulns
            if get_hash_from_typed(vuln) in duplicated_hashes
            and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        ]
        open_duplicates_hashes = [
            get_hash_from_typed(vuln) for vuln in open_duplicates
        ]
        open_duplicates_hashes_with_treatment = [
            get_hash_from_typed(vuln)
            for vuln in open_duplicates
            if vuln.treatment
            and vuln.treatment.status != VulnerabilityTreatmentStatus.UNTREATED
        ]
        closed_duplicates = [
            vuln
            for vuln in vulns
            if vuln.state.status == VulnerabilityStateStatus.SAFE
            and vuln.treatment
            and vuln.treatment.status != VulnerabilityTreatmentStatus.UNTREATED
            and get_hash_from_typed(vuln) in duplicated_hashes
            and get_hash_from_typed(vuln) in open_duplicates_hashes
            and get_hash_from_typed(vuln)
            not in open_duplicates_hashes_with_treatment
        ]
        closed_duplicates_hashes = [
            get_hash_from_typed(vuln) for vuln in closed_duplicates
        ]
        vulns_to_delete = [
            vuln
            for vuln in vulns
            if vuln.id not in unique_ids
            and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and get_hash_from_typed(vuln) in closed_duplicates_hashes
            and get_hash_from_typed(vuln) in open_duplicates_hashes
            and vuln.treatment
            and vuln.treatment.status == VulnerabilityTreatmentStatus.UNTREATED
        ]
        for vuln in closed_duplicates:
            states = await loaders.vulnerability_historic_state.load(vuln.id)
            await update_historic_entry(
                current_value=vuln,
                finding_id=finding.id,
                entry=states[-2],
                vulnerability_id=vuln.id,
            )
            await remove_state(
                vulnerability_id=vuln.id, date=states[-1].modified_date
            )
        if vulns_to_delete:
            await collect(
                tuple(
                    remove_vulnerability(
                        loaders,
                        finding.id,
                        vuln.id,
                        justification=(VulnerabilityStateReason.DUPLICATED),
                        email="drestrepo@fluidattacks.com",
                        source=Source.MACHINE,
                    )
                    for vuln in vulns_to_delete
                ),
            )
            LOGGER_CONSOLE.info(
                "Finding processed",
                extra={
                    "extra": {
                        "group_name": group_name,
                        "finding_id": finding.id,
                        "duplicated": len(vulns_to_delete),
                        "closed": len(vulns_to_delete),
                    }
                },
            )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups: List[str] = [
        group.name for group in await get_all_active_groups(loaders)
    ]  # Masked

    for group_name in groups:
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
