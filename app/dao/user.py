from __future__ import absolute_import
from boto3 import resource
from botocore.exceptions import ClientError
# pylint: disable=E0402
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY
)
import rollbar


DYNAMODB_RESOURCE = resource('dynamodb',
                             aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
                             aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
                             region_name='us-east-1')


def get_organization(email):
    """ Get the company of a user. """
    table = DYNAMODB_RESOURCE.Table('FI_users')
    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
        item = response['Item']['company']
    except ClientError:
        rollbar.report_exc_info()
    return item
