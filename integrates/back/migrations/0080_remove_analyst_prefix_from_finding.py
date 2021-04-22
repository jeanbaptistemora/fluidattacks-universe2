"""
This migration removes the api prefix for some analysts
into the finding historic state

Execution Time:    2021-03-01 at 16:09:50 UTC-05
Finalization Time: 2021-03-01 at 16:24:29 UTC-05
"""
# Standard libraries
import copy
from pprint import pprint
from typing import (
    Dict,
    cast,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend.typing import (
    Finding,
    Historic,
)
from dynamodb import operations_legacy as dynamodb_ops
from findings import dal as findings_dal


FINDING_TABLE: str = 'FI_findings'


async def remove_analyst_prefix_from_historic_state(
    finding: Dict[str, Finding]
) -> bool:
    success = True
    to_update = False
    finding_id = finding['finding_id']
    prefix = 'api-'
    old_historic_state = cast(Historic, finding.get('historic_state', []))
    historic_state = copy.deepcopy(old_historic_state)

    for state_info in historic_state:
        if state_info.get('analyst', '').startswith(prefix):
            to_update = True
            state_info['analyst'] = state_info['analyst'][len(prefix):]

    if to_update:
        success = await findings_dal.update(
            finding_id,
            {
                'historic_state': historic_state
            }
        )
        print(f'finding_id = {finding_id}')
        print('old_historic_state =')
        pprint(old_historic_state)
        print('historic_state =')
        pprint(historic_state)

    return success


async def main() -> None:
    scan_attrs = {
        'ProjectionExpression': ','.join({'finding_id', 'historic_state'})
    }
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)

    success = all(await collect(
        [
            remove_analyst_prefix_from_historic_state(finding)
            for finding in findings
        ]
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
