# pylint: disable=invalid-name
# type: ignore
"""
Remove vulnerabilities with the snippet as str

Execution Time:    2022-12-07 at 23:00:41 UTC
Finalization Time: 2022-12-07 at 23:06:07 UTC
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
    Source,
)
from organizations import (
    domain as orgs_domain,
)
import time
from vulnerabilities.domain.snippet import (
    set_snippet,
)


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings = await loaders.group_drafts_and_findings.load(group)
    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings]
    )
    vulns = tuple(
        vuln
        for vuln in vulns
        if vuln.state.source == Source.MACHINE and vuln.state.snippet is False
    )
    if vulns:
        print(f"Processing {len(vulns)} for {group}")
        await collect(
            [set_snippet(vuln, vuln.state, None) for vuln in vulns],
            workers=100,
        )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect(
        [process_group(group) for group in reversed(groups)], workers=20
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
