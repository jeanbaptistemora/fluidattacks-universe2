# pylint: disable=invalid-name
"""
This migration aims to get a list of all the current finding's titles. Deleted
and Masked findings are excluded from the search.

Similar to migration 0108, but using the new db model.

Execution Time:     2021-10-26 at 15:31:05 UTC
Finalization Time:  2021-10-26 at 15:31:21 UTC
"""

from aioextensions import (
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
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import time
from typing import (
    List,
)


async def main() -> None:

    group_names = sorted(await groups_domain.get_alive_group_names())
    print(f"   === groups: {len(group_names)}")

    loaders: Dataloaders = get_new_context()
    findings: List[Finding] = list(
        chain.from_iterable(
            await loaders.group_findings.load_many(group_names)
        )
    )
    print(f"   === findings: {len(findings)}")

    drafts: List[Finding] = list(
        chain.from_iterable(await loaders.group_drafts.load_many(group_names))
    )
    print(f"   === drafts: {len(drafts)}")

    findings.extend(drafts)
    print(f"   === findings + drafts: {len(findings)}")

    findings_info = [
        {
            "group": finding.group_name,
            "finding_id": finding.id,
            "title": finding.title,
            "status": finding.state.status.value,
        }
        for finding in findings
    ]

    csv_columns = ["group", "finding_id", "title", "status"]
    csv_file = "0152.csv"
    success = False
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in findings_info:
                writer.writerow(data)
        success = True
    except IOError:
        print("   === I/O error")

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
