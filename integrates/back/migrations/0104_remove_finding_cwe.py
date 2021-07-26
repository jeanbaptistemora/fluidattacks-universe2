# pylint: disable=invalid-name
"""
This migration aims to remove cwe field from finding
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Finding,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings.dal import (
    update,
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
import time
from typing import (
    Dict,
    List,
)

# Constants
PROD: bool = False


async def _update_finding(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding["finding_id"])
    data_to_update: Dict[str, Finding] = {"cwe": None}
    if PROD:
        print(
            "Updating finding",
            finding_id,
            data_to_update,
        )
        await update(finding_id, data_to_update)


async def update_findings(*, groups: List[str], loaders: Dataloaders) -> None:
    findings = await loaders.group_findings.load_many(groups)
    drafts = await loaders.group_drafts.load_many(groups)
    groups_findings: List[Dict[str, Finding]] = list(
        chain.from_iterable(filter(None, findings + drafts))
    )
    await collect(
        [_update_finding(finding) for finding in groups_findings],
        workers=20,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await get_active_groups()
    await collect(
        [
            update_findings(groups=list_group, loaders=loaders)
            for list_group in chunked(groups, 20)
        ],
        workers=20,
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
