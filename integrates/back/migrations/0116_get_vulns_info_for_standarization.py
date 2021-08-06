# pylint: disable=invalid-name
""",
Extract info related to vulns in findings of type `HTTP headers`,
previous to a future migration processing these vulns

Execution Time:
Finalization Time:
""",

from aioextensions import (
    collect,
    run,
)
import csv
from custom_types import (
    Finding as FindingType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups.dal import (
    get_active_groups,
)
from itertools import (
    chain,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

PROD: bool = False


async def process_finding(
    context: Dataloaders,
    finding: Dict[str, FindingType],
) -> List[Dict[str, str]]:
    finding_vulns_loader = context.finding_vulns_all
    vulns = await finding_vulns_loader.load(finding["id"])

    if len(vulns) == 0:
        print(f'   --- WARNING no vulns in finding: {finding["id"]}')
        return [{}]

    vulns_info = [
        {
            "group_name": finding["project_name"],
            "finding_id": finding["id"],
            "finding_name": finding["title"],
            "vuln_uuid": vuln["UUID"],
            "specific": vuln["specific"],
        }
        for vuln in vulns
    ]
    return vulns_info


async def process_group(
    context: Any,
    group_name: str,
) -> List[Dict[str, str]]:
    TITLE_TO_MATCH: str = "HTTP headers"
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group_name)
    filtered = [
        finding for finding in findings if TITLE_TO_MATCH in finding["finding"]
    ]
    vulns_info = list(
        chain.from_iterable(
            await collect(
                process_finding(
                    context,
                    finding,
                )
                for finding in filtered
            )
        )
    )
    print(
        f"   === group: {group_name}, "
        f"findings: {len(filtered)}, "
        f"vulns: {len(vulns_info)}"
    )
    return vulns_info


async def main() -> None:
    context: Dataloaders = get_new_context()
    groups = sorted(await get_active_groups())
    print(f"   === groups: {len(groups)}:\n{groups}")

    total = list(
        chain.from_iterable(
            await collect(
                process_group(
                    context,
                    group,
                )
                for group in groups
            )
        )
    )
    print(f"   === total vulns to write: {len(total)}")

    csv_columns = [
        "group_name",
        "finding_id",
        "finding_name",
        "vuln_uuid",
        "specific",
    ]
    csv_file = "0116_vuln_info_aug_06.csv"
    success = False
    try:
        with open(csv_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in total:
                writer.writerow(data)
        success = True
    except IOError:
        print("   === I/O error")

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z",
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z",
    )
    print(f"{execution_time}\n{finalization_time}")
