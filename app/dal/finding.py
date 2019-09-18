""" DAL functions for findings """

from __future__ import absolute_import
from datetime import datetime

import pytz
import rollbar
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# pylint:disable=relative-import
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY, FI_AWS_S3_BUCKET
)
from app.dal.helpers import s3


DYNAMODB_RESOURCE = boto3.resource(
    service_name='dynamodb',
    aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
    region_name='us-east-1')
TABLE = DYNAMODB_RESOURCE.Table('FI_findings')


def create(analyst_email, finding_id, project_name, title, **kwargs):
    success = False
    try:
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
        finding = {
            'analyst': analyst_email,
            'cvss_version': '3',
            'exploitability': 0,
            'files': [],
            'finding': title,
            'finding_id': finding_id,
            'project_name': project_name,
            'report_date': today,
            'report_level': 'GENERAL'
        }
        finding.update(kwargs)
        response = TABLE.put_item(Item=finding)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create new draft',
                               'error', extra_data=ex, payload_data=locals())
    return success


def get_finding(finding_id):
    """ Retrieve all attributes from a finding """
    response = TABLE.get_item(Key={'finding_id': finding_id})

    return response.get('Item', {})


def save_evidence(file_object, file_name):
    success = s3.upload_memory_file(FI_AWS_S3_BUCKET, file_object, file_name)

    return success


def migrate_evidence(file_path, file_name):
    success = s3.upload_stored_file(FI_AWS_S3_BUCKET, file_path, file_name)

    return success


def search_evidence(file_name):
    return s3.list_files(FI_AWS_S3_BUCKET, file_name)


def remove_evidence(file_name):
    return s3.remove_file(FI_AWS_S3_BUCKET, file_name)


def download_evidence(file_name, file_path):
    s3.download_file(FI_AWS_S3_BUCKET, file_name, file_path)


def request_verification(finding_id):
    success = False
    try:
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
        response = TABLE.update_item(
            Key={'finding_id': finding_id},
            UpdateExpression='SET verification_request_date = :req_date',
            ExpressionAttributeValues={':req_date': today})
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Verification request failed',
                               'error', extra_data=ex, payload_data=locals())
    return success


def verify(finding_id):
    success = False
    try:
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
        response = TABLE.update_item(
            Key={'finding_id': finding_id},
            UpdateExpression='SET verification_date = :verif_date',
            ExpressionAttributeValues={':verif_date': today})
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Finding verification failed',
                               'error', extra_data=ex, payload_data=locals())
    return success
