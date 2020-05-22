from typing import List
import rollbar
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('integrates')


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
    Returns the first group name available
    """
    key_exp = Key('pk').eq('AVAILABLE_GROUP')
    response = TABLE.query(
        KeyConditionExpression=key_exp,
        ProjectionExpression='sk',
        Limit=1)
    return response.get('Items', [])[0].get('sk', '').lower()


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
