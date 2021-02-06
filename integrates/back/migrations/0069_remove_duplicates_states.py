"""
This migration aims to remove consecutive duplicate states in historic_state

Execution Time: 2021-02-05 at 19:37:12 UTC-5
Finalization Time: 2021-02-05 at 20:05:28 UTC-5
"""
# Standard library
from itertools import chain
from operator import itemgetter
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
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.dal import vulnerability as vuln_dal
from backend.domain.project import (
    get_alive_projects,
)
from backend.domain.vulnerability import (
    list_vulnerabilities_async,
)
from backend.typing import (
    Finding,
)
STAGE: str = os.environ['STAGE']


async def _remove_duplicate_state(vuln: Dict[str, Finding]) -> None:
    finding_id: str = str(vuln['finding_id'])
    vuln_id: str = str(vuln['UUID'])
    historic_state = vuln['historic_state']
    historic_state_without_duplicate = [historic_state[0]]
    for state in historic_state:
        if (historic_state_without_duplicate[-1]['state'] != state['state'] or
                'approval_status' in historic_state_without_duplicate[-1]):
            historic_state_without_duplicate.append(state)

    if len(historic_state) > len(historic_state_without_duplicate):
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                {'historic_state': historic_state_without_duplicate}
            )
        else:
            print(f'should update historic_state from {vuln_id}')


async def remove_duplicate_state(groups: List[str]) -> None:
    groups_findings = await GroupFindingsLoader().load_many(groups)
    groups_drafts = await GroupDraftsLoader().load_many(groups)
    findings_ids = list(chain.from_iterable(
        [map(itemgetter('finding_id'), findings)
        for findings in groups_findings]
    ))
    drafts_ids = list(chain.from_iterable(
        [map(itemgetter('finding_id'), drafts) for drafts in groups_drafts]
    ))

    vulns = await list_vulnerabilities_async(
        findings_ids + drafts_ids,
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    await collect(map(_remove_duplicate_state, vulns), workers=10)


async def main() -> None:
    groups = await get_alive_projects()
    await collect(
        [remove_duplicate_state(list_group)
         for list_group in chunked (groups, 5)],
        workers=10
    )


if __name__ == '__main__':
    run(main())
