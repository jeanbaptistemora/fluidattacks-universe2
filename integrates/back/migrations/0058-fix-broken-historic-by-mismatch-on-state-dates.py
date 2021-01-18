"""
This migration aims to fix the historics states on
vulnerabilities changed for skims

Normal case:
    dates before date range
    +
    dateA: close by skims
    dateB: open by skims
    +
    dates after date range
Expected output:
    dates before date range + dates after date range

Special case 1:
    dates before date range
    +
    dateA: close by skims
    dateB: open by skims
    dateC: state by skims
    +
    dates after date range
Expected output:
    dates before date range + dateC + dates after date range

This works with N num of cases on the range, where normal
case works when the states has is pair, for each close one
open, that means the length of the historics to delete should
be pair, the special case works when the legth of the historics
to delete is odd, and keep the last state, because should be
a neccesary state.

This migration makes sure that the new_historic couldn't be
empty, that makes that new vulns added on that dates don't
have any problem.

Execution Time:    2021-01-17 at 16:30:22 UTC-05
Finalization Time: 2021-01-17 at 16:50:35 UTC-05
"""
# Standard library
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
    in_thread,
    run,
)

# Local libraries
from backend.dal import vulnerability as vuln_dal
from backend.domain import (
    vulnerability as vulnerability_domain,
)
from backend.typing import Vulnerability
STAGE = os.environ['STAGE']
ANALYST = 'daguirre@fluidattacks.com'
FINDING_IDS = ['899615837']


# Sort historics by date
def sort_historic_by_date(
    historic: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    historic_sort = sorted(historic, key=lambda i: i['date'])
    return historic_sort


# Get the date or return the default date
def get_date_with_format(item: Dict[str, str]) -> str:
    return str(item.get('date', '2000-01-01 00:00:00'))


# Return the desired historic
def get_historic_attribute(
    vulnerability: Vulnerability,
    attribute: str
) -> List[Dict[str, str]]:
    return cast(
        List[Dict[str, str]],
        vulnerability.get(f'historic_{attribute}', [])
    )


def filter_by_analyst(
    historic_state: Dict[str, str]
) -> bool:
    analyst = historic_state.get('analyst', '')
    if ANALYST not in analyst:
        return True
    return False


# Function to proccess all data to fix the vulnerability
# historics dates
async def fix_vuln_historics(
    vulnerability: Vulnerability,
) -> None:
    historic_state = get_historic_attribute(vulnerability, 'state')
    result_historic = sort_historic_by_date(list(
        filter(filter_by_analyst, historic_state)
    ))
    if result_historic and result_historic != historic_state:
        first_state = result_historic[0]
        if first_state['state'] == 'closed':
            date = first_state['date'].split(' ')[0]
            fixed_state = {
                'date': f'{date} 00:00:00',
                'analyst': ANALYST,
                'state': 'open',
            }
            result_historic = [fixed_state] + result_historic
            uuid = vulnerability['UUID']
            finding_id = vulnerability['finding_id']
            if STAGE == 'apply':
                print(
                    '[INFO] historic_state of vuln with UUID: ' +
                    f'{uuid} on finding: {finding_id} will be changed'
                )
                await vuln_dal.update(
                    finding_id,
                    uuid,
                    {'historic_state': result_historic}
                )
            else:
                print(
                    '[INFO] historic_state of vuln with UUID: ' +
                    f'{uuid} on finding: {finding_id} will be changed'
                )
                print('-'*20)
                print('new_historic:')
                print(result_historic)
                print('old_historic:')
                print(historic_state)
                print('-'*20)


async def main() -> None:
    print('[INFO] Starting migration 0058')
    vulneabilities = await vulnerability_domain.list_vulnerabilities_async(
        FINDING_IDS
    )
    await collect(
        [
            fix_vuln_historics(vuln) for vuln in vulneabilities
        ],
        workers=4
    )
    print('[INFO] Migration 0058 finished')

if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
