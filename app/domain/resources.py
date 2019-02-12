"""Domain functions for resources."""
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import datetime
import base64
from __init__ import FI_CLOUDFRONT_ACCESS_KEY, FI_CLOUDFRONT_PRIVATE_KEY
from cryptography.hazmat.primitives import (
    hashes, serialization, asymmetric
)
from cryptography.hazmat.backends import default_backend
from botocore.signers import CloudFrontSigner


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
    cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expire_date)
    return signed_url
