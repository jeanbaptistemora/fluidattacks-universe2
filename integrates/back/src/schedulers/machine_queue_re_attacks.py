from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from groups.domain import (
    get_active_groups,
)
from newutils.utils import (
    get_key_or_fallback,
)
from schedulers.common import (
    info,
    machine_queue,
)
import skims_sdk
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
        findings: Tuple[
            Finding, ...
        ] = await dataloaders.group_findings_new.load(group)
        for finding in findings:
            finding_id: str = finding.id
            finding_title: str = finding.title

            info(f"{group}-{finding_id}")

            vulns_to_reattack = [
                vuln
                for vuln in await dataloaders.finding_vulns.load(finding_id)
                for vuln_hv in [vuln.get("historic_verification", [])]
                if vuln["source"] in ["skims", "machine"]
                if vuln_hv
                if vuln_hv[-1].get("status") == "REQUESTED"
            ]

            if vulns_to_reattack:
                for root in await get_root_nicknames_for_skims(
                    dataloaders=dataloaders,
                    group=get_key_or_fallback(finding),
                    vulnerabilities=vulns_to_reattack,
                ):
                    finding_code = skims_sdk.get_finding_code_from_title(
                        finding_title
                    )
                    if finding_code is not None:
                        await machine_queue(
                            finding_code=finding_code,
                            group_name=group,
                            namespace=root,
                            urgent=True,
                        )
