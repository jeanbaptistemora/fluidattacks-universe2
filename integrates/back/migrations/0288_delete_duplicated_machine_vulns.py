# pylint: disable=invalid-name,too-many-function-args
# type: ignore

"""
Removes duplicate vulnerabilities reported by Machine, based on four criteria:
    - Duplicate vulnerabilities that are closed
    - Duplicate vulnerabilities that are open and do not have treatment or ZR
    - Duplicate vulnerabilities that are open while there is a confirmed ZR
    - Duplicate vulnerabilities that have some treatment defined

Execution Time:    2022-09-29 at 00:37:14 UTC
Finalization Time: 2022-09-29 at 02:42:38 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from itertools import (
    chain,
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
from vulnerabilities import (
    domain as vulns_domain,
)


def get_duplicates(
    vulns_by_idx: Dict[int, Vulnerability]
) -> Dict[int, List[Vulnerability]]:
    unique_items: List[Tuple[str, str]] = []
    original_vulns: List[int] = []
    duplicated_vulns: Dict[int, List[Vulnerability]] = {}
    for idx, vuln in vulns_by_idx.items():
        where: str = vuln.where.split(" [", maxsplit=1)[0]
        if (item := (where, vuln.specific, vuln.root_id)) not in unique_items:
            unique_items.append(item)
            original_vulns.append(idx)
        else:
            vuln_idx = original_vulns[unique_items.index(item)]
            if vuln_idx not in duplicated_vulns:
                duplicated_vulns.update({vuln_idx: [vuln]})
            else:
                duplicated_vulns[vuln_idx].append(vuln)

    return duplicated_vulns


def get_closed_duplicates(vulns: List[Vulnerability]) -> List[Vulnerability]:
    closed_vulns_by_idx: Dict[int, Vulnerability] = {
        idx: vuln
        for idx, vuln in enumerate(vulns)
        if vuln.state.status == VulnerabilityStateStatus.SAFE
    }
    duplicates = get_duplicates(closed_vulns_by_idx)

    return list(chain.from_iterable(duplicates.values()))


def get_new_open_duplicates(vulns: List[Vulnerability]) -> List[Vulnerability]:
    new_open_vulns_by_idx: Dict[int, Vulnerability] = {
        idx: vuln
        for idx, vuln in enumerate(vulns)
        if (
            vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.treatment
            and vuln.treatment.status == VulnerabilityTreatmentStatus.UNTREATED
            and (
                vuln.zero_risk is None
                or vuln.zero_risk.status
                == VulnerabilityZeroRiskStatus.REJECTED
            )
        )
    }
    duplicates = get_duplicates(new_open_vulns_by_idx)

    return list(chain.from_iterable(duplicates.values()))


def get_open_with_treatment_duplicates(
    vulns: List[Vulnerability],
) -> List[Vulnerability]:
    open_vulns_by_idx: Dict[int, Vulnerability] = {
        idx: vuln
        for idx, vuln in enumerate(vulns)
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    }
    open_duplicates = get_duplicates(open_vulns_by_idx)
    open_with_treatment_duplicates: Dict[int, List[Vulnerability]] = {}
    for vuln_idx, duplicates in open_duplicates.items():
        all_vulns = [vulns[vuln_idx]] + duplicates
        eternally_accepted: List[Vulnerability] = sorted(
            all_vulns,
            key=lambda x: (
                -(
                    x.treatment is not None
                    and x.treatment.status
                    == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
                ),
                x.created_date,
            ),
        )
        if (
            (original_vuln := eternally_accepted[0])
            and original_vuln.treatment is not None
            and original_vuln.treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ):
            original_vuln_idx = vulns.index(original_vuln)
            open_with_treatment_duplicates.update(
                {original_vuln_idx: eternally_accepted[1:]}
            )
            continue

        treatment_approved: List[Vulnerability] = sorted(
            all_vulns,
            key=lambda x: (
                -(
                    x.treatment is not None
                    and x.treatment.acceptance_status
                    == VulnerabilityAcceptanceStatus.APPROVED
                ),
                x.created_date,
            ),
        )
        if (
            (original_vuln := treatment_approved[0])
            and original_vuln.treatment is not None
            and original_vuln.treatment.acceptance_status
            == VulnerabilityAcceptanceStatus.APPROVED
        ):
            original_vuln_idx = vulns.index(original_vuln)
            open_with_treatment_duplicates.update(
                {original_vuln_idx: treatment_approved[1:]}
            )
            continue

        any_treatment: List[Vulnerability] = sorted(
            all_vulns,
            key=lambda x: (
                -(
                    x.treatment is not None
                    and x.treatment.status
                    != VulnerabilityTreatmentStatus.UNTREATED
                ),
                x.created_date,
            ),
        )
        if (
            (original_vuln := any_treatment[0])
            and original_vuln.treatment is not None
            and original_vuln.treatment.status
            != VulnerabilityTreatmentStatus.UNTREATED
        ):
            original_vuln_idx = vulns.index(original_vuln)
            open_with_treatment_duplicates.update(
                {original_vuln_idx: any_treatment[1:]}
            )

    return list(chain.from_iterable(open_with_treatment_duplicates.values()))


def get_open_with_zr_duplicates(
    vulns: List[Vulnerability],
) -> List[Vulnerability]:
    open_vulns_by_idx: Dict[int, Vulnerability] = {
        idx: vuln
        for idx, vuln in enumerate(vulns)
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    }
    open_duplicates = get_duplicates(open_vulns_by_idx)
    open_with_zr_duplicates: Dict[int, List[Vulnerability]] = {}
    for vuln_idx, duplicates in open_duplicates.items():
        sorted_open_duplicates: List[Vulnerability] = sorted(
            [vulns[vuln_idx]] + duplicates,
            key=lambda x: (
                -(
                    x.zero_risk is not None
                    and x.zero_risk.status
                    == VulnerabilityZeroRiskStatus.CONFIRMED
                ),
                x.created_date,
            ),
        )
        if (
            (original_vuln := sorted_open_duplicates[0])
            and original_vuln.zero_risk is not None
            and original_vuln.zero_risk.status
            == VulnerabilityZeroRiskStatus.CONFIRMED
        ):
            original_vuln_idx = vulns.index(original_vuln)
            open_with_zr_duplicates.update(
                {original_vuln_idx: sorted_open_duplicates[1:]}
            )

    return list(chain.from_iterable(open_with_zr_duplicates.values()))


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_group_names(loaders=loaders)
    groups_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups)

    total_groups = len(groups)
    for idx, (group, findings) in enumerate(zip(groups, groups_findings)):
        print(f"Processing group {group} ({idx+1}/{total_groups})...")
        findings_vulns = await loaders.finding_vulnerabilities.load_many(
            [fin.id for fin in findings]
        )

        vulns_to_delete: List[Tuple[str, str]] = []
        for finding, vulns in zip(findings, findings_vulns):
            machine_vulns: List[Vulnerability] = sorted(
                [
                    vuln
                    for vuln in vulns
                    if vuln.state.source == Source.MACHINE
                ],
                key=lambda x: x.created_date,
            )
            if machine_vulns:
                print(f"\tProcessing finding {finding.title}")
                duplicate_vulns_to_delete = (
                    get_closed_duplicates(machine_vulns)
                    + get_new_open_duplicates(machine_vulns)
                    + get_open_with_treatment_duplicates(machine_vulns)
                    + get_open_with_zr_duplicates(machine_vulns)
                )
                vulns_ids_to_delete = set(
                    (vuln.finding_id, vuln.id)
                    for vuln in duplicate_vulns_to_delete
                )
                print(
                    "\t\t" + f"{len(vulns_ids_to_delete)} duplicates to delete"
                )
                vulns_to_delete += list(vulns_ids_to_delete)
        print("\t" + f"Deleting {len(vulns_to_delete)} vulnerabilities...")
        await collect(
            (
                vulns_domain.remove_vulnerability(
                    loaders,
                    finding_id,
                    vuln_id,
                    StateRemovalJustification.DUPLICATED,
                    "acuberos@fluidattacks.com",
                    Source.ASM,
                    True,
                )
                for finding_id, vuln_id in vulns_to_delete
            ),
            workers=15,
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
