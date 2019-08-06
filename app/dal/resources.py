from __future__ import absolute_import
# pylint:disable=relative-import
from __init__ import FI_AWS_S3_RESOURCES_BUCKET
from app.dal.helpers import s3


def search_file(file_name):
    return s3.list_files(FI_AWS_S3_RESOURCES_BUCKET, file_name)


def save_file(file_object, file_name):
    success = s3.upload_memory_file(
        FI_AWS_S3_RESOURCES_BUCKET, file_object, file_name)

    return success


def remove_file(file_name):
    return s3.remove_file(FI_AWS_S3_RESOURCES_BUCKET, file_name)
