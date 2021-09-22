# pylint: disable=invalid-name
"""
This migration indefinitely accepts vulnerabilities that belong to inactive
root. The treatment manager is set to the user that deactivated
the root.

Execution Time:    2021-09-22 at 16:00:00 UTCUTC
Finalization Time: 2021-09-22 at 17:50:0 UTCUTC
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
from newutils import (
    datetime as datetime_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from roots import (
    dal as roots_dal,
)
import time
from unreliable_indicators.enums import (
    EntityDependency as EntityDep,
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
        for finding, vulns in zip(findings, vulns_by_finding):
            finding_modified = False
            for root in inactive_roots:
                # There are active and inactive roots that share the same
                # nickname.
                # Check exclusively for vulns that belong to inactive roots
                vulns_to_accept = [
                    vuln
                    for vuln in vulns
                    if roots_dal.filter_open_and_accepted_undef_vulns(vuln)
                    and vuln["root_nickname"] == root.state.nickname
                    and vuln["root_nickname"] not in active_roots_nicknames
                ]
                if vulns_to_accept:
                    finding_modified = True
                    print(
                        "Accepting vulnerabilities in finding "
                        f"{finding['finding_id']} from root: "
                        f"{root.state.nickname}\n"
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
            if finding_modified:
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
                            EntityDep.update_vulnerabilities_treatment,
                            finding_id=finding["finding_id"],
                        ),
                        update_unreliable_indicators_by_deps(
                            EntityDep.handle_vulnerabilities_acceptation,
                            finding_id=finding["finding_id"],
                        ),
                    )
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
