"""
This migration aims to fix the historics dates on
vulnerabilities

Execution Time:
Finalization Time:
"""
# Standard library
from itertools import chain
import os
import time
from typing import (
    Dict,
    List,
    cast,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from more_itertools import chunked

# Local libraries
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.dal import vulnerability as vuln_dal
from backend.domain.project import get_active_projects
from backend.domain import (
    vulnerability as vulnerability_domain,
)
from backend.typing import Vulnerability
STAGE = os.environ['STAGE']


def sort_historic_by_date(
    historic: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    historic_sort = sorted(historic, key=lambda i: i['date'])
    return historic_sort


def get_date_with_format(item: Dict[str, str]) -> str:
    return str(item.get('date', '')).split(' ')[0]


def get_first_historic_attribute_date(
    historic_list: List[Dict[str, str]],
    attribute: str
) -> str:
    if historic_list:
        for historic in historic_list:
            if historic.get(attribute, '').lower() in {'open', 'new'}:
                return get_date_with_format(historic)
    return ''


def print_test_stage(
    finding_id: str,
    vuln_id: str,
    historic_list: List[Dict[str, str]],
    historic_name: str,
    new_historic: List[Dict[str, str]]
) -> None:
    print('*' * 50)
    print('[INFO]')
    print(f'vuln_id: {vuln_id}')
    print(f'finding_id: {finding_id}')
    print('=' * 40)
    print(f'old_{historic_name}:', end='\n  ')
    for historic in historic_list:
        for key, value in historic.items():
            print(f"'{key}': '{value}'", end='\n  ')
    print('')
    print('=' * 40)
    print(f'new_{historic_name}', end='\n  ')
    for historic in new_historic:
        for key, value in historic.items():
            print(f"'{key}': '{value}'", end='\n  ')
    print('')
    print('=' * 40)
    print('*' * 50, end='\n\n')


async def fix_vuln_historics(
    vulnerability: Vulnerability
) -> None:
    new_state = []
    new_treatment = []
    state_is_changed = False
    treatment_is_changed = False
    historic_treatment = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_treatment', [])
    )
    historic_state = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_state', [])
    )
    historic_treatment = sort_historic_by_date(historic_treatment)
    historic_state = sort_historic_by_date(historic_state)
    vuln_id = vulnerability['UUID']
    finding_id = vulnerability['finding_id']
    first_open_state = get_first_historic_attribute_date(historic_state, 'state')
    first_new_treatment = get_first_historic_attribute_date(historic_treatment, 'treatment')
    if first_open_state < first_new_treatment:
        if historic_state and historic_state[0].get('state', '') == 'open':
            historic_state[0]['date'] = f'{first_new_treatment} 00:00:00'
            print(
                f'[INFO] Change first state date {first_open_state} '
                f'for: {first_new_treatment}'
            )
        else:
            new_state.append({
              "analyst": "daguirre@fluidattacks.com",
              "date": f'{first_new_treatment} 00:00:00',
              "state": "open"
            })
            print(f'[INFO] Add first_new_treatment: {first_new_treatment}')
        state_is_changed = True
    if first_new_treatment < first_open_state:
        if historic_treatment and historic_treatment[0].get('treatment', '') == 'NEW':
            historic_treatment[0]['date'] = f'{first_open_state} 00:00:00'
            print(
                f'[INFO] Change first treatment date {first_new_treatment} '
                f'for: {first_open_state}'
            )
        else:
            new_treatment.append({
              "date": f'{first_open_state} 00:00:00',
              "treatment": "NEW"
            })
            print(f'[INFO] Add new first_open_state: {first_open_state}')
        treatment_is_changed = True
    new_state += historic_state
    new_treatment += historic_treatment
    if state_is_changed:
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                {'historic_state': historic_state}
            )
        else:
            print_test_stage(
                finding_id, vuln_id, historic_state,
                'historic_state', new_state
            )
    if treatment_is_changed:
        if STAGE == 'apply':
            await vuln_dal.update(
                finding_id,
                vuln_id,
                {'historic_treatment': historic_treatment}
            )
        else:
            print_test_stage(
                finding_id, vuln_id, historic_treatment,
                'historic_treatment', new_treatment
            )



async def fix_vulnerabilities_historics(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data['findings'] for group_data in groups_data
        )
    )
    vulneabilities = await vulnerability_domain.list_vulnerabilities_async(
        findings_ids
    )
    await collect(
        [fix_vuln_historics(vuln) for vuln in vulneabilities],
        workers=4
    )


async def main() -> None:
    print('[INFO] Starting migration 0047')
    groups = await get_active_projects()
    await collect(
        fix_vulnerabilities_historics(list_group)
        for list_group in chunked(groups, 10)
    )
    print('[INFO] Migration 0047 finished')

if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
