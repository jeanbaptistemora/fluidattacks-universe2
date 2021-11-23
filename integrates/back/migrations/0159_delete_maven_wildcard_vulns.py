# pylint: disable=invalid-name
"""
This migration deletes all SCA vulnerabilities reported in `build.gradle` files
where the version was assumed to be a wildcard.

Execution Time:     2021-11-23 at 19:47:52 UTC
Finalization Time:  2021-11-23 at 19:51:23 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    StateRemovalJustification,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from newutils import (
    requests as requests_utils,
)
import time
from typing import (
    Dict,
    NamedTuple,
)
from vulnerabilities.domain import (
    remove_vulnerability,
)

SCA_FINDINGS_IDS = ["011", "393"]


class Context(NamedTuple):
    headers: Dict[str, str]
    loaders: Dataloaders


async def main() -> None:
    context = Context(headers={}, loaders=get_new_context())
    groups = await groups_domain.get_active_groups()
    findings = list(
        chain.from_iterable(
            await context.loaders.group_findings.load_many(groups)
        )
    )
    sca_findings = list(
        filter(
            lambda x: any(x.title.startswith(id) for id in SCA_FINDINGS_IDS),
            findings,
        )
    )
    sca_vulns = await context.loaders.finding_vulns.load_many_chained(
        [finding.id for finding in sca_findings]
    )
    gradle_wildcard_vulns = list(
        filter(
            lambda x: all(
                pattern in x["where"] for pattern in ["build.gradle", "v*"]
            ),
            sca_vulns,
        )
    )
    print(f"{len(gradle_wildcard_vulns)} vulnerabilities to delete:")
    print("\t" + "\n\t".join([vuln["UUID"] for vuln in gradle_wildcard_vulns]))
    source = requests_utils.get_source(context)
    await collect(
        remove_vulnerability(
            context.loaders,
            vuln["finding_id"],
            str(vuln["UUID"]),
            StateRemovalJustification.REPORTING_ERROR,
            "acuberos@fluidattacks.com",
            source,
            True,
        )
        for vuln in gradle_wildcard_vulns
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
