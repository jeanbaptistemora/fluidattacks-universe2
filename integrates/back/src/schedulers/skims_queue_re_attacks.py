from dataloaders import (
    get_new_context,
)
from groups.domain import (
    get_active_groups,
)
from newutils.utils import (
    get_key_or_fallback,
)
from schedulers.common import (
    info,
    skims_queue,
)
from vulnerabilities.domain.utils import (
    get_root_nicknames_for_skims,
)


async def main() -> None:
    groups = await get_active_groups()
    dataloaders = get_new_context()

    for group in sorted(groups):

        for finding in await dataloaders.group_findings.load(group):
            finding_id: str = finding["finding_id"]
            finding_title: str = finding["finding"]

            info("%s-%s", group, finding_id)

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
                    await skims_queue(
                        finding_title=finding_title,
                        group_name=group,
                        namespace=root,
                        urgent=True,
                    )
