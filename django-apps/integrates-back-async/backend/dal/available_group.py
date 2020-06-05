from typing import List
import uuid
import rollbar
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from backend.exceptions import EmptyPoolGroupName
from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('integrates')


def create(group_name: str) -> bool:
    """
    Create an available group
    """
    new_item = {'pk': 'AVAILABLE_GROUP',
                'sk': group_name.upper(),
                'gsi-2-pk': 'RANDOM_AVAILABLE_GROUP_SORT',
                'gsi-2-sk': str(uuid.uuid4())}
    resp = False
    try:
        response = TABLE.put_item(Item=new_item)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create group name',
                               'error', extra_data=ex, payload_data=locals())
    return resp


def remove(group_name: str) -> bool:
    """
    Removes an available group given its name
    """
    primary_keys = {'pk': 'AVAILABLE_GROUP',
                    'sk': group_name.upper()}
    resp = False
    try:
        response = TABLE.delete_item(Key=primary_keys)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt remove group name',
                               'error', extra_data=ex, payload_data=locals())
    return resp


def get_one() -> str:
    """
    Returns a random available group name
    """
    group_name = ''
    random_uuid = str(uuid.uuid4())
    key_exp_gt = Key('gsi-2-pk').eq('RANDOM_AVAILABLE_GROUP_SORT') & \
        Key('gsi-2-sk').gt(random_uuid)
    key_exp_lt = Key('gsi-2-pk').eq('RANDOM_AVAILABLE_GROUP_SORT') & \
        Key('gsi-2-sk').lte(random_uuid)
    query_attrs = {
        'KeyConditionExpression': key_exp_gt,
        'IndexName': 'gsi-2',
        'ProjectionExpression': 'sk',
        'Limit': 1
    }
    # Make two attempts to return a name using the random uuid
    # First attempt with greater than operator
    response = TABLE.query(**query_attrs).get('Items', [])
    if response:
        group_name = response[0].get('sk', '').lower()
    else:
        # Second attempt with less than or equal operator
        query_attrs['KeyConditionExpression'] = key_exp_lt
        response = TABLE.query(**query_attrs).get('Items', [])
        if response:
            group_name = response[0].get('sk', '').lower()
        else:
            raise EmptyPoolGroupName()
    return group_name


def get_all() -> List[str]:
    """
    Returns all availale group names
    """
    key_exp = Key('pk').eq('AVAILABLE_GROUP')
    response = TABLE.query(
        KeyConditionExpression=key_exp,
        ProjectionExpression='sk')
    all_available = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            KeyConditionExpression=key_exp,
            ProjectionExpression='sk')
        all_available += response['Items']
    all_names = [available['sk'] for available in all_available]
    return all_names


def exists(group_name: str) -> bool:
    """
    Returns True if the given group name exists
    """
    response = TABLE.get_item(Key={
        'pk': 'AVAILABLE_GROUP',
        'sk': group_name.upper()})
    return bool(response.get('Item', {}))
