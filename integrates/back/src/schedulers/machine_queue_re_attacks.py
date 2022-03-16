from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from groups.domain import (
    get_active_groups,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_job_new,
)
from schedulers.common import (
    info,
)
from typing import (
    List,
    Set,
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_root_nicknames_for_skims,
)


async def main() -> None:
    dataloaders: Dataloaders = get_new_context()

    groups: List[str] = await get_active_groups()
    groups_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await dataloaders.group_findings.load_many(groups)

    for group, findings in zip(groups, groups_findings):
        info(f"Processing group {group}...")
        findings_vulns = await dataloaders.finding_vulnerabilities.load_many(
            [finding.id for finding in findings]
        )
        findings_to_reattack: Set[str] = set()
        roots_to_reattack: Set[str] = set()
        for finding, vulns in zip(findings, findings_vulns):
            vulns_to_reattack = tuple(
                vuln
                for vuln in vulns
                if vuln.state.source == Source.MACHINE
                and vuln.verification
                and vuln.verification.status
                == VulnerabilityVerificationStatus.REQUESTED
            )

            if vulns_to_reattack:
                findings_to_reattack.add(finding.title)
                roots_to_reattack.update(
                    await get_root_nicknames_for_skims(
                        dataloaders=dataloaders,
                        group=group,
                        vulnerabilities=vulns_to_reattack,
                    )
                )

        finding_codes: Tuple[str, ...] = tuple(
            filter(
                None,
                [
                    get_finding_code_from_title(title)
                    for title in findings_to_reattack
                ],
            )
        )
        if finding_codes:
            info("\t" + f"Queueing reattacks for group {group}...")
            await queue_job_new(
                finding_codes=finding_codes,
                group_name=group,
                roots=list(roots_to_reattack),
            )
