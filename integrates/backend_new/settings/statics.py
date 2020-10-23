import os
from __init__ import (
    FI_ENVIRONMENT
)


CI_COMMIT_REF_NAME = os.environ['CI_COMMIT_REF_NAME']

TEMPLATES_DIR = 'backend_new/app/templates'

STATIC_BUCKET_NAME = 'fluidintegrates-static'
AWS_STORAGE_BUCKET_NAME = f'{STATIC_BUCKET_NAME}-{CI_COMMIT_REF_NAME}'
AWS_S3_CUSTOM_DOMAIN = 'd1l3f50ot7vyg9.cloudfront.net'
AWS_S3_SUBPATH = '/integrates/static'
if FI_ENVIRONMENT == 'production':
    AWS_S3_CUSTOM_DOMAIN = 'd1l3f50ot7vyg9.cloudfront.net'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}{AWS_S3_SUBPATH}'
else:
    STATIC_URL = (
        f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com{AWS_S3_SUBPATH}'
    )
