"""
This migration fix the attribute state for historic_state of findings

Execution Time: 2020-12-09 15:29:18 UTC-5
Finalization Time: 2020-12-09 15:46:37 UTC-5
"""
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
from backend.domain.project import get_active_projects
from backend.domain.vulnerability import list_vulnerabilities_async
from backend.utils.datetime import DEFAULT_STR

STAGE: str = os.environ['STAGE']
FINDINGS_TABLE = 'FI_findings'


async def main() -> None:
    active_groups = await get_active_projects()
    scan_attrs = {
        'ProjectionExpression': ','.join({'finding_id', 'historic_state', 'project_name'})
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
        is_finding_in_active_group = bool(finding.get('project_name', '') in active_groups)

        for index, state_info in enumerate(historic_state):
            if 'state' not in state_info:
                to_update = True
                if 'date' in state_info and 'analyst' in state_info:
                    if not is_finding_in_active_group:
                        state_info['state'] = 'Masked'
                    elif index == 0:
                        state_info['state'] = 'CREATED'
                    elif previous_state in {'REJECTED', 'CREATED'}:
                        state_info['state'] = 'SUBMITTED'
                    elif previous_state == 'SUBMITTED':
                        state_info['state'] = 'REJECTED'
                    elif previous_state == 'APPROVED':
                        state_info['state'] = 'DELETED'
                elif index == 0:
                    if is_finding_in_active_group:
                        state_info['state'] = 'CREATED'
                    else:
                        state_info['state'] = 'Masked'
                    if 'date' not in state_info:
                        vulns = await list_vulnerabilities_async(
                            [finding_id],
                            should_list_deleted=True,
                            include_confirmed_zero_risk=True,
                            include_requested_zero_risk=True
                        )
                        vuln_creation_dates = [
                            vuln.get('historic_state', [{}])[0].get('date', '')
                            for vuln in vulns
                        ]
                        vuln_creation_dates = [
                            creation_date
                            for creation_date in vuln_creation_dates
                            if creation_date
                        ]
                        if vuln_creation_dates:
                            finding_creation_date = min(vuln_creation_dates)
                        else:
                            finding_creation_date = DEFAULT_STR
                        state_info['date'] = finding_creation_date
                    if 'analyst' not in state_info:
                        if is_finding_in_active_group:
                            state_info['analyst'] = 'unknown@fluidattacks.com'
                        else:
                            state_info['analyst'] = 'Masked'
            previous_state = state_info.get('state', '')

        historic_state = [
            state_info
            for state_info in historic_state
            if 'state' in state_info
        ]

        if to_update:
            print(f'finding_id = {finding_id}')
            print(f'In active group {is_finding_in_active_group}')
            print(f'Group {finding.get("project_name", "")}')
            print('old_historic_state =')
            pprint(old_historic_state)
            print('historic_state =')
            pprint(historic_state)
            updates.append(
                update(finding_id, {"historic_state": historic_state})
            )

    print(f'Success: {all(await collect(updates, workers=64))}')


if __name__ == '__main__':
    run(main())
