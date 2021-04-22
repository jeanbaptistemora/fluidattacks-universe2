"""
This migration tries to restore some
masked data on DELETED projects.


Execution Time:    2021-03-04 at 09:23:37 UTC-05
Finalization Time: 2021-03-04 at 09:27:43 UTC-05
"""
# Standard libraries
import copy
import time
from pprint import pprint
from typing import (
    cast,
    Dict,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import Attr, Key

# Local libraries
from backend.typing import (
    Finding,
    Historic,
)
from dynamodb import operations_legacy as dynamodb_ops
from findings import dal as findings_dal
from vulnerabilities import dal as vulns_dal


FINDINGS_TABLE: str = 'FI_findings'
FINDINGS_TABLE_COPY: str = 'fi_findings_copy2'
VULNS_TABLE: str = 'FI_vulnerabilities'
VULNS_TABLE_COPY: str = 'fi_vulnerabilities_copy'


async def restore_historic_state(
    item: Dict[str, Finding],
    type_item: str,
) -> bool:
    success = True
    to_update = False
    finding_id = item['finding_id']
    vuln_uuid = item.get('UUID', '')
    prefix = 'api-'
    old_historic_state = cast(Historic, item.get('historic_state', []))
    historic_state = copy.deepcopy(old_historic_state)

    restore_table = await dynamodb_ops.query(FINDINGS_TABLE_COPY, {
            'KeyConditionExpression': Key('finding_id').eq(finding_id)
        }) if type_item == 'finding' else await dynamodb_ops.query(VULNS_TABLE_COPY, {
            'IndexName': 'gsi_uuid',
            'KeyConditionExpression': Key('UUID').eq(vuln_uuid)
        })

    r_old_historic_state = cast(Historic, restore_table[0].get('historic_state', []))
    r_historic_state = copy.deepcopy(r_old_historic_state)

    for state_info, r_state_info in zip(historic_state, r_historic_state):
        if state_info.get('analyst', '').startswith(prefix):
            to_update = True
            state_info['analyst'] = state_info['analyst'][len(prefix):]
        if state_info.get('analyst', '') == 'Masked':
            to_update = True
            state_info['analyst'] = r_state_info['analyst']
        if state_info.get('state', '') == 'Masked':
            to_update = True
            state_info['state'] = r_state_info['state']

    if to_update:
        if type_item == 'finding':
            success = await findings_dal.update(
                finding_id,
                {
                    'historic_state': historic_state
                }
            )
            print(f'finding_id = {finding_id}')
        else:
            success = await vulns_dal.update(
                finding_id,
                vuln_uuid,
                {
                    'historic_state': historic_state
                }
            )
            print(f'vuln_uuid = {vuln_uuid}')
        print('old_historic_state =')
        pprint(old_historic_state)
        print('historic_state =')
        pprint(historic_state)

    return success


async def main() -> None:
    groups_to_restore = [
        'whitehorse',
        'cankuzo',
        'varvarin',
        'dazmur',
        'ubombo',
        'denver',
        'tisina',
        'quincy',
        'alvin',
        'kalaheo',
        'chaoyang',
        'manati',
        'sylvania',
        'sylvester',
        'chickasha',
        'vaduz',
        'stornoway',
        'loudon',
        'saldus',
        'jember',
        'mandera',
        'sandy',
        'albury',
        'sarapul',
        'pomona',
        'yushel',
        'latur',
        'orillia',
        'anthem',
        'tatui',
    ]

    findings = [
        finding
        for group in groups_to_restore
        for finding in await dynamodb_ops.query('FI_findings', {
            'IndexName': 'project_findings',
            'KeyConditionExpression': Key('project_name').eq(group)
        })
    ]

    success_findings = all(await collect(
        [
            restore_historic_state(finding, 'finding')
            for finding in findings
        ]
    ))

    vulns = [
        vuln
        for finding in findings
        for vuln in await dynamodb_ops.query(VULNS_TABLE_COPY, {
            'KeyConditionExpression': Key('finding_id').eq(finding['finding_id'])
        })
    ]

    success_vulns = all(await collect(
        [
            restore_historic_state(vuln, 'vuln')
            for vuln in vulns
        ]
    ))

    print(f'Success findings: {success_findings}')
    print(f'Success vulns: {success_vulns}')


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
