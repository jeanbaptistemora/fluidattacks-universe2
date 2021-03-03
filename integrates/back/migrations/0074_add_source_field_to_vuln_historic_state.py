"""
This migration uses the analyst and the date to populate the source field
into the vulnerability historic state

Execution Time:    2021-02-22 at 16:27:03 UTC-05
Finalization Time: 2021-02-23 at 10:29:38 UTC-05
"""
# Standard library
import copy
from pprint import pprint
from typing import (
    cast,
)

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
    Historic
)
from newutils import datetime as datetime_utils


VULNERABILITY_TABLE = 'FI_vulnerabilities'


async def add_source_field_to_historic_state(
    vuln: Vulnerability
) -> bool:
    success = True
    to_update = False
    historic_state = cast(Historic, vuln.get('historic_state', []))
    old_historic_state = copy.deepcopy(historic_state)
    is_previous_api_skim_analyst = False

    for state_info in historic_state:
        if not state_info.get('source'):
            to_update = True
            is_api_skim_analyst = (
                state_info.get('analyst', '')
                in {'api-kamado@fluidattacks.com', 'api-drestrepo@fluidattacks.com'}
            )
            is_skim_analyst = (
                state_info.get('analyst', '')
                in {'kamado@fluidattacks.com', 'drestrepo@fluidattacks.com'}
            )
            if is_api_skim_analyst:
                is_previous_api_skim_analyst = True
            if (
                (
                    is_api_skim_analyst
                    or (
                        is_previous_api_skim_analyst and is_skim_analyst
                    )
                )
                and (
                    datetime_utils.get_from_str(state_info['date'])
                    > datetime_utils.get_from_str('2020-08-20 00:00:00')
                )
            ):
                state_info['source'] = 'skims'
            else:
                state_info['source'] = 'integrates'

    if to_update:
        success = await vuln_dal.update(
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
            add_source_field_to_historic_state(vuln)
            for vuln in vulns
        ]
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
