"""Domain functions for resources."""
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import datetime
import base64
import urllib
import threading
import boto3
from botocore import exceptions, signers
from cryptography.hazmat.primitives import (hashes, serialization, asymmetric)
from cryptography.hazmat.backends import default_backend
import rollbar

from app import util
from app.exceptions import ErrorUploadingFileS3, InvalidFileSize
from __init__ import (FI_CLOUDFRONT_ACCESS_KEY, FI_CLOUDFRONT_PRIVATE_KEY,
                      FI_AWS_S3_RESOURCES_BUCKET, FI_AWS_S3_ACCESS_KEY,
                      FI_AWS_S3_SECRET_KEY)

from ..dal import integrates_dal
from ..mailer import send_mail_resources

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
    filename = urllib.quote_plus(str(file_name))
    url = domain + "/" + filename
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
        raise ErrorUploadingFileS3()


def delete_file_from_s3(file_url):
    try:
        CLIENT_S3.delete_object(Bucket=BUCKET_S3, Key=file_url)
        return True
    except exceptions.ClientError:
        rollbar.report_exc_info()
        return False


def format_resource(resource_list, resource_type):
    resource_description = []
    for resource_item in resource_list:
        if resource_type == 'repository':
            repo_url = resource_item.get('urlRepo')
            repo_branch = resource_item.get('branch')
            resource_text = 'Repository: {repository!s} Branch: {branch!s}'\
                            .format(repository=repo_url, branch=repo_branch)
        elif resource_type == 'environment':
            resource_text = resource_item.get('urlEnv')
        elif resource_type == 'file':
            resource_text = resource_item.get('fileName')
        resource_description.append({'resource_description': resource_text})
    return resource_description


def send_mail(project_name, user_email, resource_list, action, resource_type):
    recipients = integrates_dal.get_project_users(project_name.lower())
    admins = [user[0] for user in integrates_dal.get_admins()]
    mail_to = [x[0] for x in recipients if x[1] == 1]
    mail_to += admins
    resource_description = format_resource(resource_list, resource_type)
    if resource_type == 'repository' and len(resource_list) > 1:
        resource_type = 'repositories'
    elif len(resource_list) > 1:
        resource_type = '{}s'.format(resource_type)
    else:
        # resource_type is the same
        pass
    context = {
        'project': project_name.lower(),
        'user_email': user_email,
        'action': action,
        'resource_type': resource_type,
        'resource_list': resource_description,
        'project_url':
            'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
        .format(project=project_name)
    }
    threading.Thread(name='Remove repositories email thread',
                     target=send_mail_resources,
                     args=(mail_to, context,)).start()


def validate_file_size(uploaded_file, file_size):
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    response = False
    if uploaded_file.size > file_size * mib:
        raise InvalidFileSize()
    else:
        response = True
    return response
