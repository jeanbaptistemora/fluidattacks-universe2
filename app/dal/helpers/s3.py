from __future__ import absolute_import
import os

import boto3
import rollbar
from botocore.exceptions import ClientError
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile
)

from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
)

CLIENT = boto3.client(
    service_name='s3',
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY)
BUCKET = FI_AWS_S3_BUCKET


def list_files(name=None):
    resp = CLIENT.list_objects_v2(Bucket=BUCKET, Prefix=name)
    key_list = [item['Key'] for item in resp.get('Contents', [])]

    return key_list


def remove_file(name):
    success = False
    try:
        CLIENT.delete_object(Bucket=BUCKET, Key=name)
        success = True
    except ClientError as ex:
        rollbar.report_message('Error: Remove from s3 failed',
                               'error', extra_data=ex, payload_data=locals())

    return success


def _send_to_s3(file_object, file_name):
    success = False
    try:
        repeated_files = list_files(file_name)
        for name in repeated_files:
            remove_file(name)
        CLIENT.upload_fileobj(file_object, BUCKET, file_name)
        success = True
    except ClientError as ex:
        rollbar.report_message('Error: Upload to s3 failed',
                               'error', extra_data=ex, payload_data=locals())

    return success


def upload_memory_file(file_object, file_name):
    success = False
    if isinstance(file_object, (InMemoryUploadedFile, TemporaryUploadedFile)):
        success = _send_to_s3(file_object.file, file_name)
    else:
        rollbar.report_message('Error: Attempt to upload invalid memory file',
                               'error', payload_data=locals())

    return success


def upload_stored_file(file_path, name):
    success = False
    try:
        file_path = '/tmp/{name}.tmp'.format(name=name)

        with open(file_path, 'r') as file_object:
            _send_to_s3(file_object, name)
        os.unlink(file_path)
        success = True
    except IOError as ex:
        rollbar.report_message('Error: Attempt to upload nonexistent file',
                               'error', extra_data=ex, payload_data=locals())

    return success
