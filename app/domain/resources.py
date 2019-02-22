"""Domain functions for resources."""
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import datetime
import base64
import boto3
import rollbar

from app import util
from __init__ import (FI_CLOUDFRONT_ACCESS_KEY, FI_CLOUDFRONT_PRIVATE_KEY,
                      FI_AWS_S3_RESOURCES_BUCKET, FI_AWS_S3_ACCESS_KEY,
                      FI_AWS_S3_SECRET_KEY)
from botocore import (
    exceptions, signers
)
from cryptography.hazmat.primitives import (
    hashes, serialization, asymmetric
)
from cryptography.hazmat.backends import default_backend

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

BUCKET_S3 = FI_AWS_S3_RESOURCES_BUCKET


def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        base64.b64decode(FI_CLOUDFRONT_PRIVATE_KEY),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, asymmetric.padding.PKCS1v15(), hashes.SHA1())


def sign_url(domain, file_name, expire_mins):
    url = domain + '/' + str(file_name)
    key_id = FI_CLOUDFRONT_ACCESS_KEY
    now_time = datetime.datetime.utcnow()
    expire_date = now_time + datetime.timedelta(minutes=expire_mins)
    cloudfront_signer = signers.CloudFrontSigner(key_id, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expire_date)
    return signed_url


def upload_file_to_s3(upload, fileurl):
    repeated_files = util.list_s3_objects(CLIENT_S3, BUCKET_S3, fileurl)
    if repeated_files:
        for k in repeated_files:
            delete_file_from_s3(k)
    try:
        CLIENT_S3.upload_fileobj(upload.file, BUCKET_S3, fileurl)
        return True
    except exceptions.ClientError:
        rollbar.report_exc_info()
        return False


def delete_file_from_s3(file_url):
    try:
        CLIENT_S3.delete_object(Bucket=BUCKET_S3, Key=file_url)
        return True
    except exceptions.ClientError:
        rollbar.report_exc_info()
        return False
