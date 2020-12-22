#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to copy external_bts from
finding to vulnerability

Execution Time:    2020-11-12 13:22:45 UTC-5
Finalization Time: 2020-11-12 13:31:12 UTC-5
"""
# Standard library
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
from backend.dal import vulnerability as vuln_dal
from backend.domain.finding import (
    get_findings_async,
)
from backend.domain.project import (
    get_active_projects,
    list_findings,
)
from backend.domain.vulnerability import (
    list_vulnerabilities_async,
)
from backend.typing import Finding
STAGE: str = os.environ['STAGE']


async def _copy_external_bts(
    finding_id: str,
    finding: Dict[str, Finding],
    vuln: Dict[str, Finding],
) -> None:
    external_bts = finding.get('externalBts', '')
    vuln_external_bts = vuln.get('external_bts', '')
    vuln_id = str(vuln.get('UUID', ''))
    if external_bts and not vuln_external_bts:
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                {'external_bts': external_bts}
            )


async def copy_external_bts(groups: List[str]) -> None:
    findings_id = await list_findings(groups)
    findings = await get_findings_async(
        finding_id
        for finding_group in findings_id
        for finding_id in finding_group
    )
    for finding in findings:
        finding_id: str = str(finding.get('findingId'))
        vulns = await list_vulnerabilities_async([finding_id])
        await collect(
            [_copy_external_bts(finding_id, finding, vuln)
            for vuln in vulns],
            workers=10
        )


async def main() -> None:
    groups = await get_active_projects()
    await collect([
        copy_external_bts(list_group)
        for list_group in chunked(groups, 10)
    ])


if __name__ == '__main__':
    run(main())
