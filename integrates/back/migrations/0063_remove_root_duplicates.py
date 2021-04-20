"""
This migration aims to remove duplicates in fi_roots that resulted from
a mistake in a previous migration script

Execution Time: 2021-01-22 at 12:05:42 UTC-05
Finalization Time: 2021-01-22 at 12:07:05 UTC-05
"""
# Standard library
import os
import time

# Third party libraries
from aioextensions import collect, run
from boto3.dynamodb.conditions import Key

# Local libraries
from backend.dal.helpers import dynamodb
from backend.typing import DynamoDelete
from groups import dal as groups_dal


STAGE = os.environ['STAGE']


async def migrate(group_name: str) -> None:
    duplicated_roots = await dynamodb.async_query(
        'fi_roots',
        {
            'KeyConditionExpression': (
                Key('pk').eq(f'GROUP#GROUP#{group_name}') &
                Key('sk').begins_with('ROOT#')
            ),
        }
    )

    if duplicated_roots:
        if STAGE == 'test':
            print(
                '[INFO] Will remove',
                len(duplicated_roots),
                'roots for',
                group_name
            )
        else:
            await collect(
                dynamodb.async_delete_item(
                    'fi_roots',
                    DynamoDelete(
                        Key={
                            'pk': root['pk'],
                            'sk': root['sk']
                        }
                    )
                )
                for root in duplicated_roots
            )


async def main() -> None:
    print('[INFO] Starting migration 0063')
    groups = await groups_dal.get_all(data_attr='project_name')
    await collect(
        migrate(group['project_name'])
        for group in groups
    )
    print('[INFO] Migration 0063 finished')


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
