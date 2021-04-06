"""
This migration set the finding release date in the vuln historic state
for those dates that are previous to the finding release

Execution Time:    2021-01-05 at 09:11:57 UTC-05
Finalization Time: 2021-01-05 at 15:46:35 UTC-05
"""
# Standard library
import copy
import os
from asyncio import run
from pprint import pprint

# Third party library
from aioextensions import collect

# Local
from backend.dal.helpers import dynamodb
from backend.filters import finding as finding_filters
from newutils import datetime as datetime_utils
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)


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
        release_date = None
        release_date_str = finding_filters.get_approval_date(finding)
        if release_date_str:
            release_date = datetime_utils.get_from_str(release_date_str)
        vulns = await vulns_domain.list_vulnerabilities_async(
            [finding_id],
            should_list_deleted=True,
            include_requested_zero_risk=True,
            include_confirmed_zero_risk=True
        )
        for vuln in vulns:
            vuln_id = vuln['UUID']
            old_historic_state = vuln.get('historic_state', [])
            historic_state = copy.deepcopy(old_historic_state)
            to_update = False

            for state_info in historic_state:
                date = datetime_utils.get_from_str(state_info['date'])
                if release_date and date < release_date:
                    state_info['date'] = release_date_str
                    to_update = True

            if to_update:
                print(f'finding_id = {finding_id}')
                print(f'release_date_str = {release_date_str}')
                print(f'vuln_id = {vuln_id}')
                print('old_historic_state =')
                pprint(old_historic_state)
                print('historic_state =')
                pprint(historic_state)
                updates.append(
                    vulns_dal.update(
                        finding_id,
                        vuln_id,
                        {"historic_state": historic_state}
                    )
                )

    print(f'Success: {all(await collect(updates, workers=64))}')


if __name__ == '__main__':
    run(main())
