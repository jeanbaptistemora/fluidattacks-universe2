# pylint: disable=invalid-name
"""
This migration deletes duplicate findings created when the Skims findings DB
and the main vulnerabilities DB were not in sync.

Execution Time:    2021-10-13 at 23:09:00 UTCUTC
Finalization Time: 2021-10-13 at 22:16:00 UTCUTC
"""

import asyncio
from context import (
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateJustification,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from typing import (
    Dict,
    Set,
)
import yaml  # type: ignore


class Context:  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.headers: Dict[str, str] = {}
        self.loaders: Dataloaders = get_new_context()


def get_vulnerabilities_database() -> Set[str]:
    vulns_file = (
        "makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml"
    )
    with open(vulns_file, "rb") as f:
        vulns = yaml.safe_load(f)
    return {f"{key}. {vulns[key]['en']['title']}" for key in vulns.keys()}


async def main() -> None:
    context = Context()
    groups = await groups_domain.get_active_groups()
    print("Loading findings...")
    all_findings = chain.from_iterable(
        await context.loaders.group_findings_new.load_many(groups)
    )
    vuln_db = get_vulnerabilities_database()
    misnamed_findings = [
        finding
        for finding in all_findings
        if (
            finding.title not in vuln_db
            and not finding.title.startswith("F")
            and finding.group_name not in FI_TEST_PROJECTS
        )
    ]
    print("Loading finding vulnerabilities...")
    finding_vulns = await context.loaders.finding_vulns.load_many(
        [finding.id for finding in misnamed_findings]
    )
    machine_findings = [
        all(vuln["source"] in {"machine", "skims"} for vuln in vulns)
        for vulns in finding_vulns
    ]
    print(
        f"Findings with issues: {len(misnamed_findings)}\n"
        f"Findings to delete: {len(list(filter(None, machine_findings)))}"
    )
    for finding, is_machine in zip(misnamed_findings, machine_findings):
        if is_machine:
            print(
                f"Deleting finding {finding.id} - {finding.title} "
                f"from group {finding.group_name}"
            )
            await findings_domain.remove_finding(
                context,
                finding.id,
                FindingStateJustification.DUPLICATED,
                "acuberos@fluidattacks.com",
            )
        else:
            print(f"{finding.group_name} - {finding.title} - {finding.id}")


if __name__ == "__main__":
    asyncio.run(main())
