# pylint: disable=invalid-name
"""
This migration aims to populate vulns from FI_vulnerabilities to
integrates_vms.

We'll keep deleted items out of the new model while we define the path
going forward for archived data.
Details at https://gitlab.com/fluidattacks/product/-/issues/5690

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from groups import (
    domain as groups_domain,
)
import time

PROD: bool = False


def _log(vuln: Vulnerability, progress: float, result: bool) -> str:
    msg = f"{vuln.finding_id},{vuln.id},{progress:.4f},{result}"
    print(msg)
    return msg


async def _process_vulnerability(
    loaders: Dataloaders,
    vuln: Vulnerability,
    progress: float,
) -> str:
    if vuln.state.status == VulnerabilityStateStatus.DELETED:
        return _log(vuln, progress, False)

    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    historic_state = await state_loader.load(vuln.id)
    historic_treatment = await treatment_loader.load(vuln.id)
    historic_verification = await verification_loader.load(vuln.id)
    historic_zero_risk = await zero_risk_loader.load(vuln.id)

    if not PROD:
        return _log(vuln, progress, False)

    await vulns_model.add(vulnerability=vuln)

    await vulns_model.update_historic(
        finding_id=vuln.finding_id,
        historic=historic_state,
        vulnerability_id=vuln.id,
    )
    if historic_treatment:
        await vulns_model.update_historic(
            finding_id=vuln.finding_id,
            historic=historic_treatment,
            vulnerability_id=vuln.id,
        )
    if historic_verification:
        await vulns_model.update_historic(
            finding_id=vuln.finding_id,
            historic=historic_verification,
            vulnerability_id=vuln.id,
        )
    if historic_zero_risk:
        await vulns_model.update_historic(
            finding_id=vuln.finding_id,
            historic=historic_zero_risk,
            vulnerability_id=vuln.id,
        )

    return _log(vuln, progress, True)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await groups_domain.get_active_groups())
    print(f"groups({len(group_names)}): {group_names[:3]}")

    findings_loader = loaders.group_drafts_and_findings
    findings = await findings_loader.load_many_chained(group_names)
    finding_ids = [finding.id for finding in findings]
    print(f"findings({len(finding_ids)}): {finding_ids[:3]}")

    vulns_to_migrate = await loaders.finding_vulns_typed.load_many_chained(
        finding_ids
    )
    print(f"vulns to migrate({len(vulns_to_migrate)}): {vulns_to_migrate[:1]}")

    results = await collect(
        _process_vulnerability(
            loaders=loaders,
            vuln=vuln,
            progress=index / len(vulns_to_migrate),
        )
        for index, vuln in enumerate(vulns_to_migrate)
    )
    print(f"results({len(results)})")

    csv_file = "0165_results.csv"
    with open(csv_file, "w", encoding="utf8") as f:
        for item in results:
            f.write(f"{item}\n")

    print("done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
