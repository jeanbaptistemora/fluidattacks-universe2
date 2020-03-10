"""DAL functions for findings."""

from decimal import Decimal
from typing import Dict, List, Union
import rollbar
from backend.typing import Finding as FindingType
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.dal.helpers import s3, dynamodb
from __init__ import FI_AWS_S3_BUCKET

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_findings')
TABLE_VULNS = DYNAMODB_RESOURCE.Table('FI_vulnerabilities')


def _escape_alnum(string: str) -> str:
    """ Removes non-alphanumeric characters from a string """
    return ''.join([char for char in string if char.isalnum()])


def create(finding_id: str, project_name: str, finding_attrs: Dict[str, FindingType]) -> bool:
    success = False
    try:
        finding_attrs.update({
            'finding_id': finding_id,
            'project_name': project_name
        })
        response = TABLE.put_item(Item=finding_attrs)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create draft',
                               'error', extra_data=ex, payload_data=locals())
    return success


def update(finding_id: str, data: Dict[str, FindingType]) -> bool:
    success = False
    primary_keys = {'finding_id': finding_id}
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = [f'{attr} = :{_escape_alnum(attr)}' for attr in data]
            values = {f':{_escape_alnum(attr)}': data[attr] for attr in data}

            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt update finding',
                               'error', extra_data=ex, payload_data=locals())

    return success


def list_append(finding_id: str, attr: str, data: List[FindingType]) -> bool:
    """
    Adds elements to the end of a list attribute

    :param finding_id: id of the finding to update
    :param attr: attribute name
    :param data: list with the elements to append
    """
    success = False
    primary_keys = {'finding_id': finding_id}
    try:
        response = TABLE.update_item(
            Key=primary_keys,
            UpdateExpression=f'SET {attr} = list_append({attr}, :data)',
            ExpressionAttributeValues={':data': data})
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt update finding',
                               'error', extra_data=ex, payload_data=locals())

    return success


def delete(finding_id: str) -> bool:
    success = False
    try:
        response = TABLE.delete_item(Key={'finding_id': finding_id})
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt delete finding',
                               'error', extra_data=ex, payload_data=locals())

    return success


def get_vulnerabilities(finding_id: str) -> List[Dict[str, FindingType]]:
    """Get vulnerabilities of a finding."""
    filtering_exp = Key('finding_id').eq(finding_id)
    response = TABLE_VULNS.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE_VULNS.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items


def get_attributes(finding_id: str, attributes: List[str]) -> Dict[str, FindingType]:
    """ Get a group of attributes of a finding. """
    item_attrs: Dict[str, Union[List[str], Dict[str, str]]] = {
        'Key': {'finding_id': finding_id},
    }
    if attributes:
        item_attrs['AttributesToGet'] = attributes
    response = TABLE.get_item(**item_attrs)
    return response.get('Item', {})


def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """ Retrieve all attributes from a finding """
    response = TABLE.get_item(Key={'finding_id': finding_id})

    return response.get('Item', {})


def save_evidence(file_object: object, file_name: str) -> bool:
    return s3.upload_memory_file(FI_AWS_S3_BUCKET, file_object, file_name)  # type: ignore


def search_evidence(file_name: str) -> bool:
    return s3.list_files(FI_AWS_S3_BUCKET, file_name)  # type: ignore


def remove_evidence(file_name: str) -> bool:
    return s3.remove_file(FI_AWS_S3_BUCKET, file_name)  # type: ignore


def download_evidence(file_name: str, file_path: str):
    s3.download_file(FI_AWS_S3_BUCKET, file_name, file_path)  # type: ignore
