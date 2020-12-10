"""
This migration aims to delete historic_treatment from finding

Execution Time:
Finalization Time:
"""
# Standard library
from itertools import chain
import os
from typing import (
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from more_itertools import chunked

# Local libraries
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.dal import finding as finding_dal
from backend.domain.project import get_active_projects
from backend.typing import Finding
STAGE: str = os.environ['STAGE']


async def _delete_historic_treatment(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding['finding_id'])
    historic_treatment = finding.get('historic_treatment', [])
    if historic_treatment:
        if STAGE == 'apply':
            await finding_dal.update(
                finding_id,
                {'historic_treatment': None}
            )
        else:
            print(f'finding {finding_id} with historic_treatment')


async def delete_historic_treatment(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data['findings'] for group_data in groups_data
        )
    )
    findings = await FindingLoader().load_many(findings_ids)
    await collect(
        [_delete_historic_treatment(finding) for finding in findings],
        workers=4
    )


async def main() -> None:
    groups = await get_active_projects()
    await collect(
        delete_historic_treatment(list_group)
        for list_group in chunked(groups, 10)
    )


if __name__ == '__main__':
    run(main())
