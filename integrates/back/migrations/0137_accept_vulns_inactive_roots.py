# pylint: disable=invalid-name
"""
This migration indefinitely accepts vulnerabilities that belong to inactive
root. The treatment manager is set to the user that deactivated
the root.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from newutils import (
    datetime as datetime_utils,
    vulnerabilities as vuln_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
import time
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    dal as vulns_dal,
)


async def main() -> None:
    groups = await groups_domain.get_active_groups()
    dataloaders = get_new_context()
    for group in groups:
        print(f"\nProcessing group {group}...")

        findings = await dataloaders.group_findings.load(group)
        vulns_by_finding = await dataloaders.finding_vulns.load_many(
            [finding["finding_id"] for finding in findings]
        )
        vulns = list(chain.from_iterable(vulns_by_finding))
        open_vulns = vuln_utils.filter_open_vulns(vulns)

        roots = await dataloaders.group_roots.load(group)
        active_roots_nicknames = [
            root.state.nickname
            for root in roots
            if root.state.status == "ACTIVE"
        ]
        inactive_roots = [
            root for root in roots if root.state.status == "INACTIVE"
        ]

        sep = "\n"
        for root in inactive_roots:
            # There are active and inactive roots that share the same nickname
            # Check exclusively for vulns that belong to inactive roots
            vulns_to_accept = [
                vuln
                for vuln in open_vulns
                if vuln["root_nickname"] == root.state.nickname
                and vuln["root_nickname"] not in active_roots_nicknames
            ]
            if vulns_to_accept:
                print(
                    f"Accepting vulnerabilities root: {root.state.nickname}\n"
                    f"{sep.join([vuln['id'] for vuln in vulns_to_accept])}"
                )
            new_treatment = [
                {
                    "acceptance_status": "APPROVED",
                    "date": datetime_utils.get_now_as_str(),
                    "justification": (
                        "Automatically accepted due to belonging to an "
                        "inactive root"
                    ),
                    "treatment": "ACCEPTED_UNDEFINED",
                    "treatment_manager": root.state.modified_by,
                    "user": root.state.modified_by,
                }
            ]
            await collect(
                vulns_dal.update(
                    vuln["finding_id"],
                    vuln["id"],
                    {
                        "historic_treatment": (
                            vuln["historic_treatment"] + new_treatment
                        )
                    },
                )
                for vuln in vulns_to_accept
            )
        await collect(
            (
                redis_del_by_deps(
                    "update_vulnerabilities_treatment",
                    finding_id=finding["finding_id"],
                    group_name=group,
                ),
                redis_del_by_deps(
                    "handle_vulnerabilities_acceptation",
                    finding_id=finding["finding_id"],
                ),
                update_unreliable_indicators_by_deps(
                    EntityDependency.update_vulnerabilities_treatment,
                    finding_id=finding["finding_id"],
                ),
                update_unreliable_indicators_by_deps(
                    EntityDependency.handle_vulnerabilities_acceptation,
                    finding_id=finding["finding_id"],
                ),
            )
            for finding in findings
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
