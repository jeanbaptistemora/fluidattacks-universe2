#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to remove unnecessary attributes
from vulnerability

Execution Time:    2020-12-03 06:45:53 UTC-5
Finalization Time: 2020-12-03 07:38:29 UTC-5
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
from backend.dal import vulnerability as vuln_dal
from backend.domain.project import (
    get_active_projects,
)
from backend.domain.vulnerability import (
    list_vulnerabilities_async,
)
from backend.typing import (
    Finding,
)
STAGE: str = os.environ['STAGE']


async def _remove_vuln_attributes(
    finding_id: str,
    vuln: Dict[str, Finding],
) -> None:
    vuln_id: str = str(vuln['UUID'])
    treatment = vuln.get('treatment')
    treatment_justification = vuln.get('treatment_justification')
    treatment_manager = vuln.get('treatment_manager')
    attr_to_remove: Dict[str, Finding] = {}
    if treatment:
        attr_to_remove['treatment'] = None
    if treatment_justification:
        attr_to_remove['treatment_justification'] = None
    if treatment_manager:
        attr_to_remove['treatment_manager'] = None
    
    if attr_to_remove:
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                attr_to_remove
            )
        else:
            print(f'should remove attrs from {vuln_id}')
    


async def remove_vuln_attributes(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data['findings'] for group_data in groups_data
        )
    )
    findings = await FindingLoader().load_many(findings_ids)
    for finding in findings:
        finding_id: str = str(finding.get('finding_id'))
        vulns = await list_vulnerabilities_async([finding_id])
        await collect(
            [_remove_vuln_attributes(finding_id, vuln)
            for vuln in vulns],
            workers=2
        )


async def main() -> None:
    groups = await get_active_projects()
    await collect([
        remove_vuln_attributes(list_group)
        for list_group in chunked(groups, 10)
    ])


if __name__ == '__main__':
    run(main())
