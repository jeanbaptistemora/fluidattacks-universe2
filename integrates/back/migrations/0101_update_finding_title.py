# pylint: disable=invalid-name,import-error
"""
This migration aims to update finding title

Execution Time:    2021-07-16 at 18:14:13 UTC-05
Finalization Time: 2021-07-16 at 18:15:01 UTC-05
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
PROD: bool = True
OLD_FINDING_TITLE_EN: str = "Missing HTTP security headers"
FINDING_TITLE_EN: str = "Insecure or Unset HTTP Headers"
OLD_FINDING_TITLE_ES: str = "Cabeceras de seguridad HTTP no establecidas"
FINDING_TITLE_ES: str = "Cabeceras HTTP inseguras o no establecidas"


async def _update_findings_titles(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding["finding_id"])
    data_to_update = get_data_to_update(finding)
    if PROD:
        print(
            "Updating finding title",
            finding_id,
            finding["project_name"],
            finding["title"],
            data_to_update,
        )
        await update(finding_id, data_to_update)


def get_data_to_update(finding: Finding) -> Dict[str, Finding]:
    if OLD_FINDING_TITLE_EN in str(finding["title"]):
        return {
            "finding": str(finding["title"]).replace(
                OLD_FINDING_TITLE_EN, FINDING_TITLE_EN
            )
        }

    return {
        "finding": str(finding["title"]).replace(
            OLD_FINDING_TITLE_ES, FINDING_TITLE_ES
        )
    }


def filter_findings_title(
    *, findings: List[Dict[str, Finding]]
) -> List[Finding]:
    return [
        finding
        for finding in findings
        if OLD_FINDING_TITLE_EN in str(finding["title"])
        or OLD_FINDING_TITLE_ES in str(finding["title"])
    ]


async def update_findings_titles(
    *, groups: List[str], loaders: Dataloaders
) -> None:
    findings = await loaders.group_findings.load_many(groups)
    drafts = await loaders.group_drafts.load_many(groups)
    groups_findings: List[Dict[str, Finding]] = list(
        chain.from_iterable(filter(None, findings + drafts))
    )
    findings_filtered = filter_findings_title(findings=groups_findings)
    await collect(
        [_update_findings_titles(finding) for finding in findings_filtered],
        workers=20,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await get_active_groups()
    await collect(
        [
            update_findings_titles(groups=list_group, loaders=loaders)
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
