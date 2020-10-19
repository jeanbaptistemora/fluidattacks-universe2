"""
This migration mask the unmasked vulns reported on chartio.
Execution Time:    2020-10-19 13:20:56 UTC-5
Finalization Time: 2020-10-19 13:21:24 UTC-5
"""

from asyncio import run
import os
from typing import (
    List,
    cast,
)

from backend.domain import (
    finding as finding_domain,
    vulnerability as vuln_domain
)
from aioextensions import (
    collect,
)

STAGE: str = os.environ['STAGE']
ENVIRONMENT: str = os.environ['ENVIRONMENT']

async def main() -> None:
    print(f'[INFO] starting migration 0031')
    findings: List[str] = []
    if ENVIRONMENT == 'development':
        findings = ['560175507']  # Mock data on JSON for test
    else:
        unmask = open("app/migrations/unmasked.csv", "r")
        vulns = unmask.read().split("\n")
        unmask.close()
        findings = list(set(map(lambda x: x.split(",")[1], vulns[1:-1])))
        for finding in findings:
            print(f'[INFO] finding {finding} will be masked')
    if STAGE == 'test':
        for finding_id in findings:
            list_vulns = await vuln_domain.list_vulnerabilities_async(
                [finding_id],
                True
            )
            for vuln in list_vulns:
                print(
                    f'[INFO] vuln with UUID {vuln.get("UUID")} will be masked'
                )
    else:
        are_findings_masked = all(await collect(
            finding_domain.mask_finding(finding_id)
            for finding_id in findings
        ))
        if are_findings_masked:
            print(f'[INFO] Migration successful')
        else:
            print(f'[ERROR] Migration fails')

if __name__ == '__main__':
    run(main())
