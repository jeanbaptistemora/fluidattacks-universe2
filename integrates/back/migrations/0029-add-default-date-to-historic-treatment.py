"""
This migration adds a dafault date to those finding historic_treatments that
do not have a date.
Execution Time:    2020-09-10 17:29:15 UTC-5
Finalization Time: 2020-09-10 18:23:20 UTC-5
"""

import copy
import os
from asyncio import run
from pprint import pprint
from typing import Any

import aioboto3

from dynamodb.operations_legacy import RESOURCE_OPTIONS
from findings.dal import update


STAGE: str = os.environ['STAGE']
FINDINGS_TABLE = 'FI_findings'


async def scan(*, table_name:str, **options: Any) -> Any:
    async with aioboto3.resource(RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(table_name)
        response = await table.scan(**options)
        for elem in response.get('Items', []):
            yield elem

        while 'LastEvaluatedKey' in response:
            options['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = await table.scan(**options)
            for elem in response.get('Items', []):
                yield elem


async def main() -> None:
    async for finding in scan(table_name=FINDINGS_TABLE):
        finding_id = finding['finding_id']
        project_name = finding.get('project_name', '')
        historic_treatment = finding.get('historic_treatment', [])
        old_historic_treatment = copy.deepcopy(historic_treatment)
        to_update = False
        first_date = None
        last_date = None

        for treatment_info in historic_treatment:
            if 'date' in treatment_info:
                last_date = treatment_info['date']
                if not first_date:
                    first_date = last_date
            elif last_date:
                to_update = True
                treatment_info['date'] = last_date

        for treatment_info in historic_treatment:
            if 'date'in treatment_info:
                break
            else:
                to_update = True
                treatment_info['date'] = first_date or '0001-01-01 00:00:00'

        if to_update:
            print(f'old_historic_treatment =')
            pprint(old_historic_treatment)
            print(f'historic_treatment =')
            pprint(historic_treatment)
            print(
                f'{project_name} & fin {finding_id} - '
                f'historic_treatment / Success: '
                f'{await update(finding_id, {"historic_treatment": historic_treatment})}'
            )

if __name__ == '__main__':
    run(main())
