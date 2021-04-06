"""
This migration removes the api prefix for some analysts
in vulnerability historic state

Execution Time:    2021-02-25 at 11:04:35 UTC-05
Finalization Time: 2021-02-25 at 14:23:58 UTC-05
"""
# Standard library
import copy
from pprint import pprint
from typing import cast

# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend.dal.helpers import dynamodb
from backend.typing import (
    Historic,
    Vulnerability,
)
from vulnerabilities import dal as vulns_dal


VULNERABILITY_TABLE = 'FI_vulnerabilities'


async def remove_analyst_prefix_in_vuln_historic_state(
    vuln: Vulnerability
) -> bool:
    success = True
    to_update = False
    prefix = 'api-'
    historic_state = cast(Historic, vuln.get('historic_state', []))
    old_historic_state = copy.deepcopy(historic_state)

    for state_info in historic_state:
        if state_info.get('analyst', '').startswith(prefix):
            to_update = True
            state_info['analyst'] = state_info['analyst'][len(prefix):]

    if to_update:
        success = await vulns_dal.update(
            vuln['finding_id'],
            vuln['UUID'],
            {
                'historic_state': historic_state
            }
        )
        print(f'finding_id = {vuln["finding_id"]}')
        print(f'vuln_id = {vuln["UUID"]}')
        print('old_historic_state =')
        pprint(old_historic_state)
        print('historic_state =')
        pprint(historic_state)

    return success


async def main() -> None:
    scan_attrs = {
        'ExpressionAttributeNames': {'#id': 'UUID'},
        'ProjectionExpression': ','.join({'#id' ,'finding_id', 'historic_state'})
    }
    vulns = await dynamodb.async_scan(VULNERABILITY_TABLE, scan_attrs)

    success = all(await collect(
        [
            remove_analyst_prefix_in_vuln_historic_state(vuln)
            for vuln in vulns
        ]
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
