"""
This migration uses the vulns, the analyst and the date to populate
the source field into the finding historic state

Execution Time:    2021-02-26 at 13:10:24 UTC-05
Finalization Time: 2021-02-26 at 13:36:41 UTC-05
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
from boto3.dynamodb.conditions import Key

# Local libraries
from backend.typing import (
    Finding,
    Historic,
)
from dynamodb import operations_legacy as dynamodb_ops
from findings import dal as findings_dal
from newutils import datetime as datetime_utils


FINDING_TABLE: str = 'FI_findings'
VULNERABILITY_TABLE: str = 'FI_vulnerabilities'


async def add_source_field_to_historic_state(
    finding: Dict[str, Finding]
) -> bool:
    success = True
    to_update = False
    vulns = None
    vulns_have_skims = False
    finding_id = finding['finding_id']
    old_finding_historic_state = cast(Historic, finding.get('historic_state', []))
    finding_historic_state = copy.deepcopy(old_finding_historic_state)
    vuln_query_attrs = {
        'KeyConditionExpression': Key('finding_id').eq(finding_id),
        'ProjectionExpression': ','.join({'historic_state'}),
    }
    skims_analysts = {
        'api-kamado@fluidattacks.com',
        'api-drestrepo@fluidattacks.com',
        'kamado@fluidattacks.com',
        'drestrepo@fluidattacks.com'
    }
    for finding_state_info in finding_historic_state:
        if not finding_state_info.get('source'):
            to_update = True
            if (
                finding_state_info.get('analyst', '') in skims_analysts
                and (
                    datetime_utils.get_from_str(finding_state_info['date'])
                    > datetime_utils.get_from_str('2020-08-20 00:00:00')
                )
            ):
                if vulns == None:
                    vulns = await dynamodb_ops.query(
                        VULNERABILITY_TABLE,
                        vuln_query_attrs
                    )
                    for vuln in vulns:
                        vuln_historic_state = cast(Historic, vuln['historic_state'])
                        for vuln_state_info in vuln_historic_state:
                            if vuln_state_info['source'] == 'skims':
                                vulns_have_skims = True
                if vulns_have_skims:
                    finding_state_info['source'] = 'skims'
                else:
                    finding_state_info['source'] = 'integrates'
            else:
                finding_state_info['source'] = 'integrates'

    if to_update:
        success = await findings_dal.update(
            finding_id,
            {
                'historic_state': finding_historic_state
            }
        )
        print(f'finding_id = {finding_id}')
        print(f'skims_analysts and vulns_have_skims = {vulns_have_skims}')
        print('old_finding_historic_state =')
        pprint(old_finding_historic_state)
        print('finding_historic_state =')
        pprint(finding_historic_state)

    return success


async def main() -> None:
    scan_attrs = {
        'ProjectionExpression': ','.join({'finding_id', 'historic_state'})
    }
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)

    success = all(await collect(
        [
            add_source_field_to_historic_state(finding)
            for finding in findings
        ]
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
