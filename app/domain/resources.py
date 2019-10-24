"""Domain functions for resources."""


import base64
import datetime
import threading
import urllib.request
import urllib.parse
import urllib.error

from botocore import signers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import asymmetric, hashes, serialization

from __init__ import FI_CLOUDFRONT_ACCESS_KEY, FI_CLOUDFRONT_PRIVATE_KEY
from app.dal import resources as resources_dal
from app.domain import project as project_domain, user as user_domain
from app.exceptions import ErrorUploadingFileS3, InvalidFileSize
from app.mailer import send_mail_resources


def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        base64.b64decode(FI_CLOUDFRONT_PRIVATE_KEY),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, asymmetric.padding.PKCS1v15(), hashes.SHA1())


def sign_url(domain, file_name, expire_mins):
    filename = urllib.parse.quote_plus(str(file_name))
    url = domain + "/" + filename
    key_id = FI_CLOUDFRONT_ACCESS_KEY
    now_time = datetime.datetime.utcnow()
    expire_date = now_time + datetime.timedelta(minutes=expire_mins)
    cloudfront_signer = signers.CloudFrontSigner(key_id, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expire_date)
    return signed_url


def save_file(upload, fileurl):
    success = resources_dal.save_file(upload, fileurl)
    if not success:
        raise ErrorUploadingFileS3()

    return success


def remove_file(file_name):
    success = resources_dal.remove_file(file_name)

    return success


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
    mail_to = project_domain.get_users(project_name.lower())
    admins = user_domain.get_admins()
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
    if uploaded_file.size > file_size * mib:
        raise InvalidFileSize()
    return True
