"""
This migration removes the source field from vulnerabilities
since its historic state has the source
"""
# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend.dal.helpers import dynamodb
from backend.dal import (
    vulnerability as vuln_dal,
)
from backend.typing import (
    Vulnerability,
)

VULNERABILITY_TABLE = 'FI_vulnerabilities'


async def remove_source_field_from_vuln(
    vuln: Vulnerability
) -> bool:
    success = True
    if vuln.get('source'):
        success = await vuln_dal.update(
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
