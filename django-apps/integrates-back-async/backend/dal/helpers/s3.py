
# disable MyPy due to error "boto module has no attribute client"
#  type: ignore

import os

import boto3
import rollbar
from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile
)


from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY
)

CLIENT = boto3.client(
    service_name='s3',
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),)


def download_file(bucket, file_name, file_path):
    CLIENT.download_file(bucket, file_name, file_path)


def list_files(bucket, name=None):
    resp = CLIENT.list_objects_v2(Bucket=bucket, Prefix=name)
    key_list = [item['Key'] for item in resp.get('Contents', [])]

    return key_list


def remove_file(bucket, name):
    success = False
    try:
        response = CLIENT.delete_object(Bucket=bucket, Key=name)
        resp_code = response['ResponseMetadata']['HTTPStatusCode']
        success = resp_code in [200, 204]
    except ClientError as ex:
        rollbar.report_message('Error: Remove from s3 failed',
                               'error', extra_data=ex, payload_data=locals())

    return success


def _send_to_s3(bucket, file_object, file_name):
    success = False
    try:
        repeated_files = list_files(bucket, file_name)
        for name in repeated_files:
            remove_file(bucket, name)
        CLIENT.upload_fileobj(file_object, bucket, file_name)
        success = True
    except ClientError as ex:
        rollbar.report_message('Error: Upload to s3 failed',
                               'error', extra_data=ex, payload_data=locals())

    return success


def upload_memory_file(bucket, file_object, file_name):
    success = False
    if isinstance(file_object, (InMemoryUploadedFile, TemporaryUploadedFile, ContentFile)):
        success = _send_to_s3(bucket, file_object.file, file_name)
    else:
        rollbar.report_message('Error: Attempt to upload invalid memory file',
                               'error', payload_data=locals())

    return success
