"""
This migration aims to delete historic_treatment from finding

Execution Time:    2020-12-11 11:47:27 UTC-5
Finalization Time: 2020-12-11 11:49:21 UTC-5
"""
# Standard library
import os
from itertools import chain
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
from api.dataloaders.group import GroupLoader
from api.dataloaders.finding import FindingLoader
from backend.typing import Finding
from findings import dal as findings_dal
from groups.domain import get_active_groups


STAGE: str = os.environ['STAGE']


async def _delete_historic_treatment(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding['finding_id'])
    historic_treatment = finding.get('historic_treatment', [])
    if historic_treatment:
        if STAGE == 'apply':
            await findings_dal.update(
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
    groups = await get_active_groups()
    await collect(
        delete_historic_treatment(list_group)
        for list_group in chunked(groups, 10)
    )


if __name__ == '__main__':
    run(main())
