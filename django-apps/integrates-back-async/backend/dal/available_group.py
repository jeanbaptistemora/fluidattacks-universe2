# standard imports
from typing import List, Dict
import uuid

# third-party imports
import aioboto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import rollbar

# local imports
from backend.exceptions import EmptyPoolGroupName
from backend.dal.helpers import dynamodb

RESOURCE_OPTIONS: Dict[str, str] = dynamodb.RESOURCE_OPTIONS  # type: ignore
TABLE_NAME: str = dynamodb.TABLE_NAME  # type: ignore


async def create(group_name: str) -> bool:
    """
    Create an available group
    """
    new_item = {
        'pk': 'AVAILABLE_GROUP',
        'sk': group_name.upper(),
        'gsi-2-pk': 'RANDOM_AVAILABLE_GROUP_SORT',
        'gsi-2-sk': str(uuid.uuid4())
    }
    resp = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        try:
            response = await table.put_item(Item=new_item)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as ex:
            rollbar.report_message(
                'Error: Couldn\'nt create group name',
                'error',
                extra_data=ex,
                payload_data=locals()
            )
    return resp


async def remove(group_name: str) -> bool:
    """
    Removes an available group given its name
    """
    primary_keys = {'pk': 'AVAILABLE_GROUP',
                    'sk': group_name.upper()}
    resp = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        try:
            response = await table.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as ex:
            rollbar.report_message(
                'Error: Couldn\'nt remove group name',
                'error',
                extra_data=ex,
                payload_data=locals()
            )
    return resp


async def get_one() -> str:
    """
    Returns a random available group name
    """
    group_name = ''
    random_uuid = str(uuid.uuid4())
    key_exp_gt = (
        Key('gsi-2-pk').eq('RANDOM_AVAILABLE_GROUP_SORT') &
        Key('gsi-2-sk').gt(random_uuid)
    )
    key_exp_lt = (
        Key('gsi-2-pk').eq('RANDOM_AVAILABLE_GROUP_SORT') &
        Key('gsi-2-sk').lte(random_uuid)
    )
    query_attrs = {
        'KeyConditionExpression': key_exp_gt,
        'IndexName': 'gsi-2',
        'ProjectionExpression': 'sk',
        'Limit': 1
    }
    # Make two attempts to return a name using the random uuid
    # First attempt with greater than operator
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        response = await table.query(**query_attrs)
        response_items = response.get('Items', [])
        if response_items:
            group_name = response_items[0].get('sk', '').lower()
        else:
            # Second attempt with less than or equal operator
            query_attrs['KeyConditionExpression'] = key_exp_lt
            response = await table.query(**query_attrs)
            response_items = response.get('Items', [])
            if response_items:
                group_name = response_items[0].get('sk', '').lower()
            else:
                raise EmptyPoolGroupName()
    return group_name


async def get_all() -> List[str]:
    """
    Returns all availale group names
    """
    key_exp = Key('pk').eq('AVAILABLE_GROUP')
    all_names = []
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        response = await table.query(
            KeyConditionExpression=key_exp,
            ProjectionExpression='sk'
        )
        all_available = response['Items']
        while response.get('LastEvaluatedKey'):
            response = await table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                KeyConditionExpression=key_exp,
                ProjectionExpression='sk'
            )
            all_available += response['Items']
        all_names = [available['sk'] for available in all_available]
    return all_names


async def exists(group_name: str) -> bool:
    """
    Returns True if the given group name exists
    """
    item_exists = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        response = await table.get_item(
            Key={
                'pk': 'AVAILABLE_GROUP',
                'sk': group_name.upper()
            }
        )
        item_exists = bool(response.get('Item', {}))
    return item_exists
