# pylint: disable=invalid-name
"""
This migration addresses vulnerabilities that were open and accepted
indefinitely and, due to some Skims bugs, where closed and a new vulnerability
was reported in the same file/line.

The new open vulnerability is removed, state DELETED, and the previous
vulnerability is reopened, maintaining the existing treatment.

Execution Time:     2021-12-14 at 19:50:23 UTC
Finalization Time:  2021-12-14 at 19:59:57 UTC
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
from db_model.vulnerabilities.types import (
    VulnerabilityState,
    VulnerabilityStateStatus,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
import time
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)


async def main() -> None:
    dataloaders = get_new_context()
    active_groups = await groups_domain.get_active_groups()
    groups_findings = await dataloaders.group_findings.load_many(active_groups)
    groups_vulns = await collect(
        dataloaders.finding_vulns_typed.load_many_chained(
            [finding.id for finding in findings]
        )
        for findings in groups_findings
    )
    accepted_closed_group_vulns = [
        [
            vuln
            for vuln in vulns
            if (
                vuln.state.status.value == "CLOSED"
                and vuln.treatment.status.value == "ACCEPTED_UNDEFINED"
            )
        ]
        for vulns in groups_vulns
    ]
    locations = [
        [(vuln.finding_id, vuln.where, vuln.specific) for vuln in vulns]
        for vulns in accepted_closed_group_vulns
    ]
    new_open_groups_vulns = [
        [
            vuln
            for vuln in vulns
            if (
                vuln.state.status.value == "OPEN"
                and (vuln.finding_id, vuln.where, vuln.specific)
                in locations[idx]
                and vuln.treatment.status.value == "NEW"
            )
        ]
        for idx, vulns in enumerate(groups_vulns)
    ]

    for group, (open_vulns, accepted_closed_vulns) in zip(
        active_groups, zip(new_open_groups_vulns, accepted_closed_group_vulns)
    ):
        print(
            f"There are {len(open_vulns)} "
            f"vulnerabilities to process in group {group}:"
        )
        for vuln in open_vulns:
            accepted_vulns = list(
                filter(
                    lambda x, v=vuln: (  # type: ignore
                        x.finding_id,
                        x.where,
                        x.specific,
                    )
                    == (v.finding_id, v.where, v.specific),
                    accepted_closed_vulns,
                )
            )
            if len(accepted_vulns) == 1:
                await vulns_domain.remove_vulnerability(
                    dataloaders,
                    vuln.finding_id,
                    vuln.id,
                    StateRemovalJustification.NOT_REQUIRED,
                    "acuberos@fluidattacks.com",
                    Source.ASM,
                )
                await vulns_dal.update_state(
                    current_value=accepted_vulns[0].state,
                    finding_id=accepted_vulns[0].finding_id,
                    vulnerability_id=accepted_vulns[0].id,
                    state=VulnerabilityState(
                        modified_by="acuberos@fluidattacks.com",
                        modified_date=datetime_utils.get_iso_date(),
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                        justification=(
                            StateRemovalJustification.NO_JUSTIFICATION
                        ),
                    ),
                )
            else:
                print("\tThis vulnerability should be reviewed manually")
            print("\t" + vuln.finding_id)
            print("\t" + vuln.id)
            print("\t" + vuln.where)
            print("\t" + vuln.specific + "\n")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
