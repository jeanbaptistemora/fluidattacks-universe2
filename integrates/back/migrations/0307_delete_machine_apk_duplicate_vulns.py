# pylint: disable=invalid-name
# type: ignore
"""
Removes duplicate vulnerabilities reported by Machine in APK findings

Execution Time:    2022-10-26 at 19:37:37 UTC
Finalization Time: 2022-10-26 at 19:43:17 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time
from typing import (
    List,
    Tuple,
)
from vulnerabilities.domain import (
    remove_vulnerability,
)

duplicate_mod = __import__("0288_delete_duplicated_machine_vulns")
APK_FINDINGS: List[str] = [
    "046",
    "048",
    "055",
    "058",
    "060",
    "075",
    "082",
    "082",
    "103",
    "206",
    "207",
    "313",
    "268",
    "372",
    "398",
]


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_findings = (
        await loaders.group_drafts_and_findings.load_many_chained(list(groups))
    )
    apk_findings: List[Finding] = [
        finding
        for finding in groups_findings
        if finding.title[:3] in APK_FINDINGS
    ]
    apk_vulns = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in apk_findings]
    )
    total_findings = len(apk_findings)
    for idx, (finding, vulns) in enumerate(zip(apk_findings, apk_vulns)):
        print(f"Processing finding {idx+1}/{total_findings}...")
        machine_vulns: List[Vulnerability] = sorted(
            [vuln for vuln in vulns if vuln.state.source == Source.MACHINE],
            key=lambda x: x.created_date,
        )

        vulns_to_delete: List[Tuple[str, ...]] = []
        if machine_vulns:
            duplicate_vulns_to_delete: List[Vulnerability] = (
                duplicate_mod.get_closed_duplicates(machine_vulns)
                + duplicate_mod.get_new_open_duplicates(machine_vulns)
                + duplicate_mod.get_open_with_treatment_duplicates(
                    machine_vulns
                )
                + duplicate_mod.get_open_with_zr_duplicates(machine_vulns)
            )
            vulns_ids_to_delete = set(
                (vuln.id, vuln.where, vuln.specific)
                for vuln in duplicate_vulns_to_delete
            )
            vulns_to_delete += list(vulns_ids_to_delete)

            if vulns_to_delete:
                print(
                    "\t" + f"Deleting {len(vulns_to_delete)} vulnerabilities "
                    f"from finding {finding.title} "
                    f"in group {finding.group_name}"
                )
                print(
                    "\t\t"
                    + "\n\t\t".join(
                        [f"{vuln[1]} - {vuln[2]}" for vuln in vulns_to_delete]
                    )
                )
                await collect(
                    (
                        remove_vulnerability(
                            loaders,
                            finding.id,
                            vuln[0],
                            StateRemovalJustification.DUPLICATED,
                            "acuberos@fluidattacks.com",
                            True,
                        )
                        for vuln in vulns_to_delete
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
