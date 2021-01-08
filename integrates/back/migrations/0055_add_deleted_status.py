"""
This migration aims to add DELETED status to vulns

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
from backend.domain.finding.draft import (
    get_drafts_by_group,
)
from backend.domain.finding.finding import (
    delete_vulnerabilities,
    get_findings_by_group,
    is_deleted,
)
from backend.domain.project import (
    get_alive_projects,
)
from backend.typing import (
    Finding,
)
STAGE: str = os.environ['STAGE']


async def _add_deleted_status(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding['finding_id'])
    historic_state = finding['historic_state']
    last_state = historic_state[-1]
    if STAGE == 'apply':
        await delete_vulnerabilities(
            finding_id,
            last_state['justification'],
            last_state['analyst'],
        )
    else:
        print(f'should update vulns for finding {finding_id}')


async def add_deleted_status(group_name: str) -> None:
    attrs = {'finding_id', 'historic_state'}
    group_findings = await get_findings_by_group(
        group_name, attrs, include_deleted=True
    )
    findings = [finding for finding in group_findings if is_deleted(finding)]
    await collect(
        [_add_deleted_status(finding) for finding in findings],
        workers=5
    )


async def main() -> None:
    groups = await get_alive_projects()
    await collect(
        [add_deleted_status(group) for group in groups],
        workers=10
    )


if __name__ == '__main__':
    run(main())
