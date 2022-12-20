from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_job_new,
)
from newutils.vulnerabilities import (
    is_machine_vuln,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)
from vulnerabilities.domain.utils import (
    get_root_nicknames_for_skims,
)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    groups_findings: tuple[
        tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(group_names)

    for group_name, findings in zip(group_names, groups_findings):
        info(f"Processing group {group_name}...")
        findings_vulns = await loaders.finding_vulnerabilities.load_many(
            [finding.id for finding in findings]
        )
        findings_to_reattack: set[str] = set()
        roots_to_reattack: set[str] = set()
        for finding, vulns in zip(findings, findings_vulns):
            vulns_to_reattack = tuple(
                vuln
                for vuln in vulns
                if is_machine_vuln(vuln)
                and vuln.verification
                and vuln.verification.status
                == VulnerabilityVerificationStatus.REQUESTED
            )

            if vulns_to_reattack:
                findings_to_reattack.add(finding.title)
                roots_to_reattack.update(
                    await get_root_nicknames_for_skims(
                        loaders=loaders,
                        group=group_name,
                        vulnerabilities=vulns_to_reattack,
                    )
                )

        finding_codes: tuple[str, ...] = tuple(
            filter(
                None,
                [
                    get_finding_code_from_title(title)
                    for title in findings_to_reattack
                ],
            )
        )
        if finding_codes:
            info("\t" + f"Queueing reattacks for group {group_name}...")
            await queue_job_new(
                finding_codes=finding_codes,
                group_name=group_name,
                roots=list(roots_to_reattack),
                dataloaders=loaders,
            )
