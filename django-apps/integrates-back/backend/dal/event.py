"""DAL functions for events."""

from typing import Dict, List, Union
import rollbar
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb, s3

from __init__ import FI_AWS_S3_BUCKET

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('fi_events')

EventType = Dict[str, Union[List[Dict[str, str]], str, None]]


def create(event_id: str, project_name: str, event_attributes: EventType) -> bool:
    success = False
    try:
        event_attributes.update({
            'event_id': event_id,
            'project_name': project_name
        })
        response = TABLE.put_item(Item=event_attributes)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create event',
                               'error', extra_data=ex, payload_data=locals())
    return success


def update(event_id: str, data: EventType) -> bool:
    success = False
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key={'event_id': event_id},
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = [f'{attr} = :{attr}' for attr in data]
            values = {f':{attr}': value for attr, value in data.items()}

            response = TABLE.update_item(
                Key={'event_id': event_id},
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt update event',
                               'error', extra_data=ex, payload_data=locals())

    return success


def get_event(event_id: str) -> EventType:
    """ Retrieve all attributes from an event """
    response = TABLE.get_item(Key={'event_id': event_id})

    return response.get('Item', {})


def save_evidence(file_object: object, file_name: str) -> bool:
    return s3.upload_memory_file(FI_AWS_S3_BUCKET, file_object, file_name)  # type: ignore


def remove_evidence(file_name: str) -> bool:
    return s3.remove_file(FI_AWS_S3_BUCKET, file_name)  # type: ignore
