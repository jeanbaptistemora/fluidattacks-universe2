"""
This migration removes the source field from vulnerabilities
since its historic state has the source

Execution Time:    2021-02-24 at 11:09:24 UTC-05
Finalization Time: 2021-02-24 at 14:44:44 UTC-05
"""
# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend.dal.helpers import dynamodb
from backend.typing import Vulnerability
from vulnerabilities import dal as vulns_dal


VULNERABILITY_TABLE = 'FI_vulnerabilities'


async def remove_source_field_from_vuln(
    vuln: Vulnerability
) -> bool:
    success = True
    if vuln.get('source'):
        success = await vulns_dal.update(
            vuln['finding_id'],
            vuln['UUID'],
            {
                'source': None
            }
        )
        print(f'Removed source from {vuln["UUID"]}')

    return success


async def main() -> None:
    scan_attrs = {
        'ExpressionAttributeNames': {'#id': 'UUID', '#source': 'source'},
        'ProjectionExpression': ','.join({'#id' ,'finding_id', '#source'})
    }
    vulns = await dynamodb.async_scan(VULNERABILITY_TABLE, scan_attrs)

    success = all(await collect(
        [
            remove_source_field_from_vuln(vuln)
            for vuln in vulns
        ]
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
