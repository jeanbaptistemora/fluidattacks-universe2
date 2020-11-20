#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to copy historic_treatment from
finding to vulnerability

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
from backend.dal import vulnerability as vuln_dal
from backend.domain.project import (
    get_active_projects,
)
from backend.domain.vulnerability import (
    add_vuln_treatment,
    list_vulnerabilities_async,
)
from backend.typing import (
    Finding,
)
from backend.utils.datetime import (
    DEFAULT_STR,
    get_from_str,
)
STAGE: str = os.environ['STAGE']


async def _copy_historic_treatment(
    finding_id: str,
    finding: Dict[str, Finding],
    vuln: Dict[str, Finding],
) -> None:
    historic_treatment = finding.get('historic_treatment', [])
    vuln_historic_treatment = vuln.get('historic_treatment', [])
    vuln_id = str(vuln.get('UUID', ''))
    if vuln_historic_treatment:
        if historic_treatment:
            current_treatment = historic_treatment[-1]
            current_vuln = vuln_historic_treatment[-1]
            if (get_from_str(current_treatment.get('date', DEFAULT_STR)) >
                    get_from_str(current_vuln.get('date', DEFAULT_STR))):
                if STAGE == 'apply':
                    await add_vuln_treatment(
                        finding_id=finding_id,
                        updated_values=current_treatment,
                        vuln=vuln,
                        user_email=current_treatment.get('user', ''),
                        date=current_treatment.get('date', DEFAULT_STR),
                    )
                else:
                    print(f'treatment on finding {finding_id} is most recent'
                          f' than treatment on vuln {vuln_id}')
    elif historic_treatment:
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                {'historic_treatment': historic_treatment}
            )
        else:
            print(f'vuln {vuln_id} without historic_treatment')


async def copy_historic_treatment(groups: List[str]) -> None:
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
            [_copy_historic_treatment(finding_id, finding, vuln)
            for vuln in vulns],
            workers=5
        )


async def main() -> None:
    groups = await get_active_projects()
    await collect([
        copy_historic_treatment(list_group)
        for list_group in chunked(groups, 5)
    ])


if __name__ == '__main__':
    run(main())
