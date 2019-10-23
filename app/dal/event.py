"""DAL functions for events."""

import boto3

# pylint:disable=relative-import
from __init__ import FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY


DYNAMODB_RESOURCE = boto3.resource(
    service_name='dynamodb',
    aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
    region_name='us-east-1')
TABLE = DYNAMODB_RESOURCE.Table('fi_events')


def get_event(event_id):
    """ Retrieve all attributes from an event """
    response = TABLE.get_item(Key={'event_id': event_id})

    return response.get('Item', {})
