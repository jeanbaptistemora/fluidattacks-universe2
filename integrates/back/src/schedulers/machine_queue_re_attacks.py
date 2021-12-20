from back.src.machine.jobs import (
    get_finding_code_from_title,
)
from dataloaders import (
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from groups.domain import (
    get_active_groups,
)
from schedulers.common import (
    info,
    machine_queue,
)
from typing import (
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_root_nicknames_for_skims,
)


async def main() -> None:
    groups = await get_active_groups()
    dataloaders = get_new_context()

    for group in sorted(groups):
        findings: Tuple[Finding, ...] = await dataloaders.group_findings.load(
            group
        )
        for finding in findings:
            finding_id: str = finding.id
            finding_title: str = finding.title

            info(f"{group}-{finding_id}")

            vulns: Tuple[
                Vulnerability, ...
            ] = await dataloaders.finding_vulns_typed.load(finding_id)
            vulns_to_reattack = tuple(
                vuln
                for vuln in vulns
                if vuln.state.source == Source.MACHINE
                and vuln.verification
                and vuln.verification.status
                == VulnerabilityVerificationStatus.REQUESTED
            )

            if vulns_to_reattack:
                for root in await get_root_nicknames_for_skims(
                    dataloaders=dataloaders,
                    group=group,
                    vulnerabilities=vulns_to_reattack,
                ):
                    finding_code = get_finding_code_from_title(finding_title)
                    if finding_code is not None:
                        await machine_queue(
                            finding_code=finding_code,
                            group_name=group,
                            namespace=root,
                        )
