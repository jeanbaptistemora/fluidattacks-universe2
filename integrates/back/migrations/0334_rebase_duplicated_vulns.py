# pylint: disable=invalid-name
# type: ignore
"""
Remove machine duplicate vulnerabilities

Execution Time:    2022-12-19 at 20:00:51 UTC
Finalization Time: 2022-12-19 at 20:17:40 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Tuple,
)
from vulnerabilities.domain.core import (
    remove_vulnerability,
)
from vulnerabilities.domain.utils import (
    get_hash_from_typed,
)


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group)
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings]
    )
    closed_hash = {
        str(get_hash_from_typed(vuln)): vuln
        for vuln in vulns
        if vuln.state.source == Source.MACHINE
        and vuln.state.status == VulnerabilityStateStatus.SAFE
        and vuln.state.modified_by == "machine@fluidattacks.com"
    }
    open_hash = {
        str(get_hash_from_typed(vuln)): vuln
        for vuln in vulns
        if vuln.state.source == Source.MACHINE
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        and vuln.treatment.status == VulnerabilityTreatmentStatus.NEW
        and vuln.treatment.modified_by in ("machine@fluidattacks.com", None)
    }
    duplicates = []
    for duplicated_hash in set(closed_hash.keys()).intersection(
        open_hash.keys()
    ):
        open_vuln = open_hash[duplicated_hash]
        closed_vuln = closed_hash[duplicated_hash]
        states: Tuple[
            VulnerabilityState,
        ] = await loaders.vulnerability_historic_state.load(closed_vuln.id)
        if len(states) < 2:
            continue
        await update_historic_entry(
            current_value=closed_vuln,
            finding_id=closed_vuln.finding_id,
            entry=states[-2],
            vulnerability_id=closed_vuln.id,
        )
        await operations.batch_delete_item(
            keys=(
                PrimaryKey(
                    partition_key=f"VULN#{closed_vuln.id}",
                    sort_key=(
                        f"STATE#{closed_vuln.state.modified_date.isoformat()}"
                    ),
                ),
            ),
            table=TABLE,
        )
        await remove_vulnerability(
            loaders,
            open_vuln.finding_id,
            open_vuln.id,
            StateRemovalJustification.DUPLICATED,
            "drestrepo@fluidattacks.com",
        )
        duplicates.append([group, closed_vuln.id, open_vuln.id])
    with open("bad_rebase_fix.csv", "a+", encoding="utf-8") as handler:
        writer = csv.writer(handler)
        writer.writerows(duplicates)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect([process_group(group) for group in groups], workers=15)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
