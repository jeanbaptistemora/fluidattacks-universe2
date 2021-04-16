"""
This migration aims to fix the historics dates on
vulnerabilities

This handles 4 kind of cases:

Case 1: when the historics has the default date
        see migration 0029 and 0030.

Case 2: when the treatment didn't exist or the
        histori state has no open state

Case 3: when the first treatment occur before
        the first open state.

Case 4: when the first open state occur before
        the first treatment.

When the date cannot be resolve succesfully with
the historic use the first historic state of the
finding if has historic, if not uses the date of
the lastVulnerability

Execution Time:    2020-12-20 at 14:07:09 UTC-05
Finalization Time: 2020-12-20 at 14:52:04 UTC-05
"""
# Standard library
import os
import time
from itertools import chain
from typing import (
    cast,
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    in_thread,
    run,
)
from more_itertools import chunked

# Local libraries
from backend.api.dataloaders.group import GroupLoader
from backend.typing import Vulnerability
from findings import domain as findings_domain
from groups.domain import get_active_groups
from newutils import findings as finding_utils
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)


STAGE = os.environ['STAGE']


# Sort historics by date
def sort_historic_by_date(
    historic: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    historic_sort = sorted(historic, key=lambda i: i['date'])
    return historic_sort


# Get the date or return the default date
def get_date_with_format(item: Dict[str, str]) -> str:
    return str(item.get('date', '2000-01-01 00:00:00'))


# Return the first desired historic date
def get_first_historic_attribute_date(
    historic_list: List[Dict[str, str]],
    attribute: str
) -> str:
    if historic_list:
        if attribute == 'treatment':
            return get_date_with_format(historic_list[0])
        for historic in historic_list:
            if historic.get(attribute, '').replace(' ', '_').lower() == 'open':
                return get_date_with_format(historic)
        return '2000-01-01 00:00:00'
    return '2000-01-01 00:00:00'


# Print all test data in the desired format
def print_test_stage(
    finding_id: str,
    vuln_id: str,
    old_historic: List[Dict[str, str]],
    historic_name: str,
    new_historic: List[Dict[str, str]],
    change_data: bool
) -> None:
    print('*' * 50)
    print('[INFO]')
    print(f'vuln_id: {vuln_id}')
    print(f'finding_id: {finding_id}')
    # Print old historic if is added a new entry
    if not change_data:
        print('=' * 40)
        print(f'old_{historic_name}:', end='\n  ')
        for historic in old_historic:
            for key1, value1 in historic.items():
                print(f"'{key1}': '{value1}'", end='\n  ')
        print('')
    print('=' * 40)
    print(f'new_{historic_name}', end='\n  ')
    for historic in new_historic:
        for key2, value2 in historic.items():
            print(f"'{key2}': '{value2}'", end='\n  ')
    print('')
    print('=' * 40)
    print('*' * 50, end='\n\n')


# Return the desired historic
def get_historic_attribute(
    vulnerability: Vulnerability,
    attribute: str
) -> List[Dict[str, str]]:
    return cast(
        List[Dict[str, str]],
        vulnerability.get(f'historic_{attribute}', [])
    )


# Return a boolean that say if is neccesary to handle
# the cases 1 and 2
def handle_historic_default(
    first_open_state: str,
    first_new_treatment: str,
) -> bool:
    state_is_default = is_default_date(first_open_state)
    treatment_is_default = is_default_date(first_new_treatment)
    same_dates = state_is_default and treatment_is_default
    return same_dates or not first_open_state or not first_new_treatment


# Return a boolean that say if the date is the default date
def is_default_date(date: str) -> bool:
    return date == '2000-01-01 00:00:00'


# Function to proccess all data to fix the vulnerability
# historics dates
async def fix_vuln_historics(
    vulnerability: Vulnerability,
    fix_date: str
) -> None:
    new_state = []
    new_treatment = []
    state_is_changed = False
    treatment_is_changed = False
    change_data1 = False
    change_data2 = False
    historic_treatment = get_historic_attribute(vulnerability, 'treatment')
    historic_state = get_historic_attribute(vulnerability, 'state')
    historic_treatment = sort_historic_by_date(historic_treatment)
    historic_state = sort_historic_by_date(historic_state)
    vuln_id = vulnerability['UUID']
    finding_id = vulnerability['finding_id']
    first_open_state = get_first_historic_attribute_date(historic_state, 'state')
    first_new_treatment = get_first_historic_attribute_date(historic_treatment, 'treatment')
    first_state = historic_state[0].get('state', '').lower()
    treatment_is_default = is_default_date(first_new_treatment)
    state_is_default = is_default_date(first_open_state)

    # Handle default dates or empty dates.
    if handle_historic_default(first_open_state, first_new_treatment):
        # If historic treatment exist modify the first treatment to be at
        # the same date that the fix date
        if historic_treatment:
            historic_treatment[0]['date'] = f'{fix_date} 00:00:00'
            print(
                f'[INFO] Change first treatment date {first_new_treatment} '
                f'for: {fix_date} 00:00:00'
            )
            change_data1 = True
            treatment_is_changed = True

        # If historic don't exist create a new entry with the same
        # date of the fix date
        else:
            new_treatment.append({
              "date": f'{fix_date} 00:00:00',
              "treatment": "NEW"
            })
            print(f'[INFO] Add new first_new_treatment: {fix_date}')
            treatment_is_changed = True

        # If historic exists and the first state is open
        # change the date to open the vuln on the fix date
        if historic_state and first_state == 'open':
            historic_state[0]['date'] = f'{fix_date} 00:00:00'
            print(
                f'[INFO] Change first state date {first_open_state} '
                f'for: {fix_date} 00:00:00'
            )
            change_data2 = True
            state_is_changed = True

        # If historic don't exist or the first state isn't open
        # state create a new entry with the fix date
        else:
            new_state.append({
              "analyst": "daguirre@fluidattacks.com",
              "date": f'{fix_date} 00:00:00',
              "state": "open"
            })
            print(f'[INFO] Add first_open_state: {fix_date}')
            state_is_changed = True

    # Handle when the first treatment is after the first open
    elif treatment_is_default or first_new_treatment > first_open_state \
        and not state_is_default:

        # Fix the first treatment date with the next date if the
        # treatment date is default
        if first_new_treatment == '2000-01-01 00:00:00':
            if len(historic_treatment) > 1:
                first_open_state = historic_treatment[1].get('date', '')

        # If historic treatment exist modify the first treatment to be at
        # the same date that the first open state
        if historic_treatment:
            historic_treatment[0]['date'] = f'{first_open_state}'
            print(
                f'[INFO] Change first treatment date {first_new_treatment} '
                f'for: {first_open_state}'
            )
            treatment_is_changed = True
            change_data1 = True

        # If historic don't exist create a new entry with the same
        # date of the first open to be compliant the born of the both
        # historics
        else:
            new_treatment.append({
              "date": f'{first_open_state}',
              "treatment": "NEW"
            })
            print(f'[INFO] Add new first_open_state: {first_open_state}')
            treatment_is_changed = True

    elif state_is_default or first_open_state > first_new_treatment:
        # Fix the first state date with the next date if the
        # treatment date is default
        if state_is_default:
            if len(historic_state) > 1:
                first_new_treatment = historic_treatment[1].get('date', '')

        # If historic exists and the first state is open
        # change the date to open the vuln
        # at the same date of the treatment.
        if historic_state and historic_state[0].get('state', '') == 'open':
            historic_state[0]['date'] = f'{first_new_treatment}'
            print(
                f'[INFO] Change first state date {first_open_state} '
                f'for: {first_new_treatment}'
            )
            change_data2 = True

        # If historic don't exist or the first state isn't open
        # state create a new entry with the same
        # date of the first open to be compliant the born of the both
        # historics
        else:
            new_state.append({
              "analyst": "daguirre@fluidattacks.com",
              "date": f'{first_new_treatment}',
              "state": "open"
            })
            print(f'[INFO] Add first_new_treatment: {first_new_treatment}')
        state_is_changed = True

    # Handle if the historic was changed or a new entry was created
    new_state += historic_state
    new_treatment += historic_treatment

    # Eval which historic was modified and work with it
    if treatment_is_changed:
        if STAGE == 'apply':
            print(f'vuln_id: {vuln_id}')
            print(f'finding_id: {finding_id}')
            await vulns_dal.update(
                finding_id,
                vuln_id,
                {'historic_treatment': new_treatment}
            )
        else:
            print_test_stage(
                finding_id, vuln_id, historic_treatment,
                'historic_treatment', new_treatment, change_data1
            )

    if state_is_changed:
        if STAGE == 'apply':
            print(f'vuln_id: {vuln_id}')
            print(f'finding_id: {finding_id}')
            await vulns_dal.update(
                finding_id,
                vuln_id,
                {'historic_state': new_state}
            )
        else:
            print_test_stage(
                finding_id, vuln_id, historic_state,
                'historic_state', new_state, change_data2
            )


# Get all vulnerabilities and get all dates to get a fix date in case
# that could be needed (cases 1 and 2)
async def fix_vulns(finding: str) -> None:
    vulneabilities = await vulns_domain.list_vulnerabilities_async(
        [finding]
    )
    dates = finding_utils.get_tracking_dates(vulneabilities)
    filter_dates = [
        date
        for date in dates
        if date > '2000-01-01 00:00:00'
    ]
    filter_dates.sort()
    if not filter_dates:
        finding_data = await findings_domain.get_finding(finding)
        historic_state = cast(
            List[Dict[str, str]],
            finding_data.get('historic_state', [])
        )
        if historic_state:
            filter_dates = [historic_state[0]['date']]
        else:
            filter_dates = [finding_data['lastVulnerability']]
    await collect([
        await in_thread(fix_vuln_historics, vuln, filter_dates[0])
        for vuln in vulneabilities
    ])


# Prepare the findings_ids and iterate each id on thread to be able to get
# the fix dates if is neccesary
async def fix_vulnerabilities_historics(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data['findings'] for group_data in groups_data
        )
    )
    await collect([
        await in_thread(
            fix_vulns, finding
        )
        for finding in findings_ids
    ])


async def main() -> None:
    print('[INFO] Starting migration 0047')
    groups = await get_active_groups()
    groups.sort()
    await collect([
        await in_thread(fix_vulnerabilities_historics, list_group)
        for list_group in chunked(groups, 10)
    ])
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
