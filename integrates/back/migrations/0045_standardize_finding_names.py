# pylint: disable=invalid-name,import-error
"""
This migration aims to standardize findings names

Execution Time:    2020-12-15 at 22:57:50 UTC-05
Finalization Time: 2020-12-15 at 23:00:25 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Finding,
)
from dataloaders.finding import (
    FindingLoader,
)
from dataloaders.group import (
    GroupLoader,
)
from findings import (
    dal as findings_dal,
)
from groups.domain import (
    get_active_groups,
)
from itertools import (
    chain,
)
from more_itertools import (
    chunked,
)
import os
import re
import time
from typing import (
    Dict,
    List,
)

STAGE: str = os.environ["STAGE"]


async def _standardize_finding_name(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding["finding_id"])
    finding_title = finding.get("title", "").strip()
    regex_old = r"^F.+\.([0-9]+)\."
    regex_new = r"^F[0-9]{3}\. .+"
    is_old = re.search(regex_old, finding_title)
    is_compliant = re.match(regex_new, finding_title)
    if finding_title and is_old:
        finding_num = is_old.group(1)
        while len(finding_num) != 3:
            num_chars = len(finding_num)
            if num_chars >= 4:
                finding_num = finding_num[1:]
            else:
                finding_num = f"0{finding_num}"
        replace_val = f"F{finding_num}."
        new_title = finding_title.replace(is_old.group(), replace_val)
        if STAGE == "apply":
            print(f"[INFO] Updating name for finding {finding_id}")
            await findings_dal.update(finding_id, {"finding": new_title})
        else:
            print("[INFO]")
            print(f"fiding_id: {finding_id}")
            print(f"old_title: {finding_title}")
            print(f"new_title: {new_title}")
    elif is_compliant:
        print(f"[INFO] finding with id {finding_id} is compliant")
    else:
        # The titles that didn't match is because are 'CAPEC', 'CWE' and 'WASC'
        # That titles would be mapped on a new migration.
        print(f"[ERROR]\nfinding with id {finding_id} didn't match regex")
        print(f"title: {finding_title}")


async def standardize_findings_names(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data["findings"] for group_data in groups_data
        )
    )
    findings = await FindingLoader().load_many(findings_ids)
    await collect(
        [_standardize_finding_name(finding) for finding in findings], workers=4
    )


async def main() -> None:
    print("[INFO] Starting migration 0042")
    groups = await get_active_groups()
    await collect(
        standardize_findings_names(list_group)
        for list_group in chunked(groups, 10)
    )
    print("[INFO] Migration 0042 finished")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
