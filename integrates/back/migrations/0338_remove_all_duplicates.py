# pylint: disable=invalid-name
# type: ignore
"""
Remove machine duplicate vulnerabilities

Remove all vulnerable or safe duplicates,
vulnerabilities that have treatment are preserved,
if there is a safe vulnerability and a vulnerable one, the safe one is
opened and the vulnerable one is deleted, if the oldest one is safe

Execution Time:    2022-12-23 at 13:53:41 UTC
Finalization Time: 2022-12-23 at 14:22:02 UTC
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
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Dict,
    List,
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
    vulns = [
        vuln
        for vuln in vulns
        if vuln.type == VulnerabilityType.LINES
        and vuln.hacker_email
        in ("kamado@fluidattacks.com", "machine@fluidattacks.com")
    ]

    duplicates: Dict[str, List[Vulnerability]] = {}
    for vuln in vulns:
        if vuln.zero_risk:
            continue
        vuln_hash = str(get_hash_from_typed(vuln))
        if vuln_hash not in duplicates:
            duplicates[vuln_hash] = [vuln]
        else:
            duplicates[vuln_hash].append(vuln)

    duplicates_csv = []
    for vuln_hash, vulns in duplicates.items():
        closed_vuln = None
        if (len(vulns)) < 2:
            continue
        vulns = [
            *sorted(
                [
                    x
                    for x in vulns
                    if x.treatment.status
                    != VulnerabilityTreatmentStatus.UNTREATED
                ],
                key=lambda x: x.treatment.modified_date.timestamp(),
                reverse=True,
            ),
            *sorted(
                [
                    x
                    for x in vulns
                    if x.treatment.status
                    == VulnerabilityTreatmentStatus.UNTREATED
                ],
                key=lambda x: x.state.modified_date,
            ),
        ]
        if all(
            vuln.state.status == VulnerabilityStateStatus.SAFE
            for vuln in vulns
        ) or all(
            vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            for vuln in vulns
        ):
            keep_vuln = vulns[0]
            vulns_to_delete = vulns[1:]
        elif vulns[0].state.status == VulnerabilityStateStatus.SAFE:
            keep_vuln = vulns[0]
            closed_vuln = vulns[0]
            vulns_to_delete = vulns[1:]
        else:
            keep_vuln = vulns[0]
            vulns_to_delete = vulns[1:]

        if closed_vuln:
            states: Tuple[
                VulnerabilityState,
            ] = await loaders.vulnerability_historic_state.load(closed_vuln.id)
            states = [
                state for state in states if state.source == Source.MACHINE
            ]
            if len(states) < 2:
                continue
            new_state = states[-2]
            new_state = new_state._replace(
                modified_date=datetime.utcnow(),
                modified_by="drestrepo@fluidattacks.com",
                justification=StateRemovalJustification.DUPLICATED,
            )
            await update_historic_entry(
                current_value=closed_vuln,
                finding_id=closed_vuln.finding_id,
                entry=new_state,
                vulnerability_id=closed_vuln.id,
            )
            await collect(
                [
                    remove_vulnerability(
                        loaders,
                        vuln.finding_id,
                        vuln.id,
                        VulnerabilityStateReason.DUPLICATED,
                        "drestrepo@fluidattacks.com",
                        True,
                    )
                    for vuln in vulns_to_delete
                ]
            )
            duplicates_csv.append(
                [
                    closed_vuln.group_name,
                    closed_vuln.id,
                    "MODIFY",
                    closed_vuln.state.status.value,
                    closed_vuln.state.modified_date.isoformat(),
                    closed_vuln.treatment.status.value,
                    closed_vuln.treatment.modified_date.isoformat(),
                    str(get_hash_from_typed(closed_vuln)),
                ]
            )
            duplicates_csv.extend(
                [
                    [
                        vuln.group_name,
                        vuln.id,
                        "DELETE",
                        vuln.state.status.value,
                        vuln.state.modified_date.isoformat(),
                        vuln.treatment.status.value,
                        vuln.treatment.modified_date.isoformat(),
                        str(get_hash_from_typed(vuln)),
                    ]
                    for vuln in vulns_to_delete
                ]
            )
        else:
            await collect(
                [
                    remove_vulnerability(
                        loaders,
                        vuln.finding_id,
                        vuln.id,
                        VulnerabilityStateReason.DUPLICATED,
                        "drestrepo@fluidattacks.com",
                        include_closed_vuln=True,
                    )
                    for vuln in vulns_to_delete
                ]
            )
            duplicates_csv.append(
                [
                    keep_vuln.group_name,
                    keep_vuln.id,
                    "KEEP",
                    keep_vuln.state.status.value,
                    keep_vuln.state.modified_date.isoformat(),
                    keep_vuln.treatment.status.value,
                    keep_vuln.treatment.modified_date.isoformat(),
                    str(get_hash_from_typed(keep_vuln)),
                ]
            )
            duplicates_csv.extend(
                [
                    [
                        vuln.group_name,
                        vuln.id,
                        "DELETE",
                        vuln.state.status.value,
                        vuln.state.modified_date.isoformat(),
                        vuln.treatment.status.value,
                        vuln.treatment.modified_date.isoformat(),
                        str(get_hash_from_typed(vuln)),
                    ]
                    for vuln in vulns_to_delete
                ]
            )
    with open("remove_all_duplicates.csv", "a+", encoding="utf-8") as handler:
        writer = csv.writer(handler)
        writer.writerows(duplicates_csv)


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
