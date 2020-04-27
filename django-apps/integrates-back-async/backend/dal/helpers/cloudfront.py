
import base64
from datetime import datetime, timedelta
import urllib.parse
from cryptography.hazmat.primitives import asymmetric, hashes, serialization
from cryptography.hazmat.backends import default_backend
from botocore import signers
from __init__ import (
    FI_CLOUDFRONT_ACCESS_KEY,
    FI_CLOUDFRONT_PRIVATE_KEY)


def sign_url(domain: str, file_name: str, expire_mins: float) -> str:
    filename = urllib.parse.quote_plus(str(file_name))
    url = domain + '/' + filename
    key_id = FI_CLOUDFRONT_ACCESS_KEY
    now_time = datetime.utcnow()
    expire_date = now_time + timedelta(minutes=expire_mins)
    cloudfront_signer = signers.CloudFrontSigner(key_id, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expire_date)
    return signed_url


def rsa_signer(message: str) -> bool:
    private_key = serialization.load_pem_private_key(
        base64.b64decode(FI_CLOUDFRONT_PRIVATE_KEY),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, asymmetric.padding.PKCS1v15(), hashes.SHA1())


def download_file(file_info: str, project_name: str, domain: str, expire_mins: float) -> str:
    project_name = project_name.lower()
    file_url = project_name + '/' + file_info
    return sign_url(domain, file_url, expire_mins)
