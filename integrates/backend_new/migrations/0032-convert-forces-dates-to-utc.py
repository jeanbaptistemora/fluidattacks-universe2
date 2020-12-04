"""
This migration converts all force datetimes to UTC
Execution Time:    2020-10-22 10:00:32 UTC-5
Finalization Time: 2020-10-22 10:07:52 UTC-5
"""
from typing import (
    Any,
    AsyncIterator,
    Coroutine,
    List,
    Tuple,
)

# Standard library
import asyncio

# Third party libraries
import aioboto3
from boto3.dynamodb.conditions import Key
from dateutil.parser import parse as date_parser
import pytz

# Local libraries
from backend.dal.project import get_active_projects
from backend.domain.project import get_many_groups
from backend.dal.helpers import dynamodb

# Constants
TABLE_NAME = 'bb_executions'
TABLE_NAME_NEW_FORCES = 'FI_forces'


async def yield_executions_new(project_name: str) -> AsyncIterator[Any]:
    key_condition_expresion = \
        Key('subscription').eq(project_name)

    async with aioboto3.resource(**dynamodb.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(TABLE_NAME_NEW_FORCES)
        query_params = {'KeyConditionExpression': key_condition_expresion}
        has_more = True
        while has_more:
            results = await table.query(**query_params)
            for result in results['Items']:
                yield result

            if results.get('LastEvaluatedKey', None):
                query_params['ExclusiveStartKey'] = results.get(
                    'LastEvaluatedKey')

            has_more = results.get('LastEvaluatedKey', False)


async def get_groups_with_forces() -> List[str]:
    project_names = await get_active_projects()
    groups = await get_many_groups(project_names)
    group_names = []
    for group in groups:
        configuration = group.get('historic_configuration', [])
        if not configuration:
            continue
        if not configuration[-1].get('has_forces', False):
            continue
        group_names.append(group['project_name'])
    return group_names


async def update_execution(execution: Any) -> Tuple[str, str, bool]:
    new_date = date_parser(execution['date']).astimezone(pytz.UTC)
    update_attrs = {
        "Key": {
            "subscription": execution['subscription'],
            "execution_id": execution['execution_id']
        },
        "UpdateExpression": "SET #date_field = :date_value",
        "ExpressionAttributeNames": {
            "#date_field": "date"
        },
        "ExpressionAttributeValues": {
            ":date_value": new_date.isoformat()
        }
    }
    success = await dynamodb.async_update_item(
        TABLE_NAME_NEW_FORCES,
        update_attrs,
    )
    return execution['execution_id'], execution['subscription'], success


async def get_futures() -> List[Coroutine[Any, Any, Tuple[str, str, bool]]]:
    futures = []
    groups = await get_groups_with_forces()
    for group in groups:
        async for execution in yield_executions_new(group):
            futures.append(update_execution(execution))
    return futures


async def main() -> None:
    futures = await get_futures()
    for result in asyncio.as_completed(futures):
        execution_id, group, success = await result
        if success:
            print(f'[SUCCESS] {group} {execution_id}')
        else:
            print(f'[ERROR] {group} {execution_id}')


if __name__ == '__main__':
    futures = asyncio.run(main())
