"""
This migration remove releaseDate and report_date from findings

Execution Time: 2020-12-07 16:00:25 UTC-5
Finalization Time: 2020-12-07 16:28:09 UTC-5
"""
# Standard library
import os
from asyncio import run

# Third party library
from aioextensions import collect

# Local
from backend.dal.helpers import dynamodb
from findings.dal import update


STAGE: str = os.environ['STAGE']
FINDINGS_TABLE = 'FI_findings'


async def _print_findings_with_attributes() -> None:
    scan_attrs = {
        'ProjectionExpression': ','.join(
            {'finding_id', 'releaseDate', 'report_date'}
        )
    }
    findings = await dynamodb.async_scan(FINDINGS_TABLE, scan_attrs)
    for finding in findings:
        print(finding)


async def main() -> None:
    if  STAGE == 'test':
        print('Before migration')
        await _print_findings_with_attributes()

    scan_attrs = {
        'ProjectionExpression': ','.join({'finding_id'})
    }
    updates = []
    findings = await dynamodb.async_scan(FINDINGS_TABLE, scan_attrs)
    for finding in findings:
        if (
            # We don't care about wiped findings
            finding.get('finding') == 'WIPED'
            or finding.get('affected_systems') == 'Masked'
        ):
            continue

        finding_id = finding['finding_id']
        updates.append(
            update(finding_id, {
                'releaseDate': None,
                'report_date': None
            })
        )
    print(f'Success: {all(await collect(updates, workers=64))}')

    if  STAGE == 'test':
        print('After migration')
        await _print_findings_with_attributes()


if __name__ == '__main__':
    run(main())
