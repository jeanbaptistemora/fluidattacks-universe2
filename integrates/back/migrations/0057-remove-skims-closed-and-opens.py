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
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.dal import vulnerability as vuln_dal
from backend.domain.project import get_active_projects
from backend.domain import vulnerability as vulnerability_domain
from backend.typing import Vulnerability
from newutils import findings as finding_utils


STAGE = os.environ['STAGE']
CLOSE_RANGE = ['2020-12-01 00:00:00', '2020-12-31 23:59:59']
REOPEN_RANGE = ['2020-12-01 00:00:00', '2021-01-31 23:59:59']
ANALYST = 'api'


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


def first_closed_of_month(
    historic_state: Dict[str, str]
) -> bool:
    state = historic_state['state']
    date = historic_state['date']
    analyst = historic_state.get('analyst', '')
    date_in_range = CLOSE_RANGE[0] <= date <= CLOSE_RANGE[1]
    if state == 'closed' and date_in_range and ANALYST in analyst:
        return True
    return False


def first_reopen_of_month(
    historic_state: Dict[str, str],
    closed_date: str
) -> bool:
    state = historic_state['state']
    date = historic_state['date']
    analyst = historic_state.get('analyst', '')
    date_in_range = closed_date <= date <= REOPEN_RANGE[1]
    if state == 'open' and date_in_range and ANALYST in analyst:
        return True
    return False


# Function to proccess all data to fix the vulnerability
# historics dates
async def fix_vuln_historics(
    vulnerability: Vulnerability,
) -> None:
    historic_state = get_historic_attribute(vulnerability, 'state')
    closed_by_analyst = sort_historic_by_date(list(
        filter(first_closed_of_month, historic_state)
    ))
    if closed_by_analyst:
        first_closed = closed_by_analyst[0]['date']
        reopen_by_analyst = sort_historic_by_date(list(
            filter(lambda x: first_reopen_of_month(
                x, first_closed
            ), historic_state)
        ))
        if reopen_by_analyst:
            dates_to_delete = sort_historic_by_date(
                closed_by_analyst + reopen_by_analyst
            )
            if (dates_to_delete[-1]['state'] == 'closed' or (
                len(dates_to_delete) % 2 == 1 and
                dates_to_delete[-1]['state'] == 'open'
            )):
                dates_to_delete = dates_to_delete[:-1]
            new_historic = list(
                filter(lambda x: x not in dates_to_delete, historic_state)
            )
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
                    {'historic_state': new_historic}
                )
            else:
                print(
                    '[INFO] historic_state of vuln with UUID: ' +
                    f'{uuid} on finding: {finding_id} will be changed'
                )
                print('-'*20)
                print('new_historic:')
                print(new_historic)
                print('old_historic:')
                print(historic_state)
                print('-'*20)


# Prepare the findings_ids and iterate each id on thread to be able to get
# the fix dates if is neccesary
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
        [
            fix_vuln_historics(vuln) for vuln in vulneabilities
            # if vuln['UUID'] == "549585ca-4a8f-48da-ab37-8172540e57c0"
        ],
        workers=4
    )


async def main() -> None:
    print('[INFO] Starting migration 0057')
    groups = await get_active_projects()
    groups.sort()
    await collect([
        fix_vulnerabilities_historics(list_group)
        for list_group in chunked(groups, 10)
    ])
    print('[INFO] Migration 0057 finished')

if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
