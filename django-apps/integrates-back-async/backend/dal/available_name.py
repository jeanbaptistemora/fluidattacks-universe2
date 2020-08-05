# standard imports
import logging
import uuid
from typing import List, Dict

# third-party imports
import aioboto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# local imports
from backend.exceptions import EmptyPoolName
from backend.dal.helpers import dynamodb


# Constants
LOGGER = logging.getLogger(__name__)
RESOURCE_OPTIONS: Dict[str, str] = dynamodb.RESOURCE_OPTIONS  # type: ignore
TABLE_NAME: str = dynamodb.TABLE_NAME  # type: ignore


async def create(name: str, entity: str) -> bool:
    """
    Create an available entity name
    """
    new_item = {
        'pk': f'AVAILABLE_{entity.upper()}',
        'sk': name.upper(),
        'gsi-2-pk': f'RANDOM_AVAILABLE_{entity.upper()}_SORT',
        'gsi-2-sk': str(uuid.uuid4())
    }
    resp = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        try:
            response = await table.put_item(Item=new_item)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    return resp


async def remove(name: str, entity: str) -> bool:
    """
    Removes an available entity given its name
    """
    primary_keys = {'pk': f'AVAILABLE_{entity.upper()}',
                    'sk': name.upper()}
    resp = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        try:
            response = await table.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    return resp


async def get_one(entity: str) -> str:
    """
    Returns a random available entity name
    """
    name = ''
    random_uuid = str(uuid.uuid4())
    key_exp_gt = (
        Key('gsi-2-pk').eq(f'RANDOM_AVAILABLE_{entity.upper()}_SORT') &
        Key('gsi-2-sk').gt(random_uuid)
    )
    key_exp_lt = (
        Key('gsi-2-pk').eq(f'RANDOM_AVAILABLE_{entity.upper()}_SORT') &
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
            name = response_items[0].get('sk', '').lower()
        else:
            # Second attempt with less than or equal operator
            query_attrs['KeyConditionExpression'] = key_exp_lt
            response = await table.query(**query_attrs)
            response_items = response.get('Items', [])
            if response_items:
                name = response_items[0].get('sk', '').lower()
            else:
                raise EmptyPoolName(entity)
    return name


async def get_all(entity: str) -> List[str]:
    """
    Returns all availale entity names
    """
    key_exp = Key('pk').eq(f'AVAILABLE_{entity.upper()}')
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


async def exists(name: str, entity: str) -> bool:
    """
    Returns True if the given entity name exists
    """
    item_exists = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(TABLE_NAME)
        response = await table.get_item(
            Key={
                'pk': f'AVAILABLE_{entity.upper()}',
                'sk': name.upper()
            }
        )
        item_exists = bool(response.get('Item', {}))
    return item_exists
