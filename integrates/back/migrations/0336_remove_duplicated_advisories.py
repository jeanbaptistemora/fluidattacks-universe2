# pylint: disable=invalid-name
# type: ignore
"""
Remove duplicated advisories

Execution Time:    2022-12-19 at 20:00:51 UTC
Finalization Time: 2022-12-19 at 20:17:40 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from newutils.vulnerabilities import (
    get_advisories,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Tuple,
)


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group)
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings if "011" in fin.title]
    )
    duplicates = []
    for vuln in vulns:
        if (advisories := get_advisories(vuln.state.where)) and (
            vuln.state.where.count(advisories) == 2
        ):
            await update_historic_entry(
                current_value=vuln,
                finding_id=vuln.finding_id,
                entry=vuln.state._replace(
                    where=vuln.state.where.replace(f" {advisories}", "", 1)
                ),
                vulnerability_id=vuln.id,
            )
            duplicates.append(
                [
                    group,
                    vuln.id,
                    vuln.state.where,
                    vuln.state.where.replace(f" {advisories}", "", 1),
                ]
            )
    with open(
        "remove_duplicated_advisories.csv", "a+", encoding="utf-8"
    ) as handler:
        writer = csv.writer(handler)
        writer.writerows(duplicates)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect([process_group(group) for group in groups], workers=15)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
