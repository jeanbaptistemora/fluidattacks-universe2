# pylint: disable=invalid-name
"""
This migration aims to merge duplicate findings since there was no validation
when creating drafts. Issue related
https://gitlab.com/fluidattacks/product/-/issues/5696

Vulns are copied to the oldest finding and the newer ones is deleted.

Execution Time:
Finalization Time:
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
from db_model.enums import (
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain import (
    core as findings_dom,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import time
from typing import (
    Dict,
    List,
    NamedTuple,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
import uuid
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = False


class Context(NamedTuple):
    headers: Dict[str, str]
    loaders: Dataloaders


async def update_indicators(finding_id: str) -> None:
    return await update_unreliable_indicators_by_deps(
        EntityDependency.remove_vulnerability, finding_id=finding_id
    )


async def create_vuln(
    loaders: Dataloaders,
    vuln: Vulnerability,
    target_finding_id: str,
) -> bool:
    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    historic_state = await state_loader.load(vuln.id)
    historic_treatment = await treatment_loader.load(vuln.id)
    historic_verification = await verification_loader.load(vuln.id)
    historic_zero_risk = await zero_risk_loader.load(vuln.id)
    return await vulns_dal.create_new(
        vulnerability=vuln._replace(
            finding_id=target_finding_id,
            id=str(uuid.uuid4()),
        ),
        historic_state=historic_state,
        historic_treatment=historic_treatment,
        historic_verification=historic_verification,
        historic_zero_risk=historic_zero_risk,
    )


def save_migration_info(
    duplicated_findings: List[Finding],
    target_finding: str,
    vulns: List[str],
) -> None:
    findings_info = [
        {
            "group": finding.group_name,
            "duplicated_finding_id": finding.id,
            "target_finding_id": target_finding,
            "title": finding.title,
            "vulns_to_move": len(vulns),
            "id_vulns": vulns,
        }
        for finding in duplicated_findings
    ]

    csv_columns = [
        "group",
        "duplicated_finding_id",
        "title",
        "target_finding_id",
        "vulns_to_move",
        "id_vulns",
    ]
    csv_file = "0164.csv"
    try:
        with open(csv_file, "a", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in findings_info:
                writer.writerow(data)
    except IOError:
        print("   === I/O error")


async def _get_duplicated_findings(
    context: Dataloaders, finding: Finding, group_findings: Tuple[Finding, ...]
) -> bool:
    success = True
    print(f"\n\tProcessing id # {finding.id} title: {finding.title}")
    duplicated_findings = [
        finding_item
        for finding_item in group_findings
        if finding_item.title == finding.title
        and finding_item.id != finding.id
    ]
    if not duplicated_findings:
        print("\t=== NO duplicates found")
        return True

    creation_dates = [
        fin_duplicated.creation.modified_date
        for fin_duplicated in duplicated_findings
        if fin_duplicated.creation is not None
    ]

    if finding.creation.modified_date > min(creation_dates):
        print("\tDuplicated but not the oldest one")
        return True

    vulns_load = list(
        chain.from_iterable(
            await context.loaders.finding_vulns_all_typed.load_many(
                [item.id for item in duplicated_findings]
            )
        )
    )
    uuids = [vuln.id for vuln in vulns_load]
    print(f"\t=== We found ({len(duplicated_findings)}) duplicates")
    print(
        f"""\n\t\tDuplicated Id: {[item.id for item in duplicated_findings]}
        target: {finding.id}"""
    )
    print(f"\t\tVulns to move: {len(vulns_load)}")

    if PROD and vulns_load:
        success = all(
            await collect(
                create_vuln(
                    loaders=context.loaders,
                    vuln=vuln,
                    target_finding_id=finding.id,
                )
                for vuln in vulns_load
            )
        )
        print(
            f"""\t\t=== {success} creating {len(vulns_load)}
            vulns group {finding.group_name}"""
        )

        await collect(
            findings_dom.remove_finding(
                context=context,
                finding_id=finding.id,
                justification=StateRemovalJustification.DUPLICATED,
                user_email="kcamargo@fluidattacks.com",
            )
            for finding in duplicated_findings
        )

        await update_indicators(finding.id)
    save_migration_info(duplicated_findings, finding.id, uuids)
    return success


async def process_group(context: Dataloaders, group: str) -> bool:
    findings: Tuple[Finding, ...] = await context.loaders.group_findings.load(
        group
    )
    if not findings:
        return True
    print(f"\nProcessing group {group} with {len(findings)} finding(s)...")
    return await collect(
        (
            _get_duplicated_findings(context, finding, findings)
            for finding in findings
        ),
        workers=1,
    )


async def main() -> None:
    context: Context = Context(headers={}, loaders=get_new_context())
    groups: List[str] = sorted(await groups_domain.get_active_groups())
    segment: List[str] = groups[:5]
    success: bool = all(
        await collect(
            (process_group(context, group) for group in segment), workers=1
        )
    )
    print(f"\nsuccess: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
