# Standard library
from asyncio import run
import copy
import os
from pprint import pprint

# Third party library
from aioextensions import (
    collect,
)

# Local
from backend.dal.helpers import dynamodb
from backend.dal.finding import update

STAGE: str = os.environ['STAGE']
FINDINGS_TABLE = 'FI_findings'


async def main() -> None:
    scan_attrs = {
        'ProjectionExpression': ','.join({'finding_id', 'historic_state'})
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
        old_historic_state = finding.get('historic_state', [])
        historic_state = copy.deepcopy(old_historic_state)
        to_update = False
        previous_state = ''

        for index, state_info in enumerate(historic_state):
            if 'state' not in state_info:
                to_update = True
                if index == 0:
                    state_info['state'] = 'CREATED'
                elif previous_state in {'REJECTED', 'CREATED'}:
                    state_info['state'] = 'SUBMITTED'
                elif previous_state == 'SUBMITTED':
                    state_info['state'] = 'REJECTED'
                elif previous_state == 'APPROVED':
                    state_info['state'] = 'DELETED'
            previous_state = state_info.get('state', '')

        historic_state = [
            state_info
            for state_info in historic_state
            if 'state' in state_info
        ]

        if to_update:
            print(f'finding_id = {finding_id}')
            print(f'old_historic_state =')
            pprint(old_historic_state)
            print(f'historic_state =')
            pprint(historic_state)
            updates.append(
                update(finding_id, {"historic_state": historic_state})
            )

    print(f'Success: {all(await collect(updates, workers=64))}')


if __name__ == '__main__':
    run(main())
