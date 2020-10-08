import os
from __init__ import (
    FI_DEBUG,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
    FI_MIXPANEL_API_TOKEN
)

DEBUG = FI_DEBUG == 'True'
CI_COMMIT_REF_NAME = os.environ['CI_COMMIT_REF_NAME']

TIME_ZONE = 'America/Bogota'

# JWT
JWT_COOKIE_NAME = "integrates_session"
JWT_COOKIE_SAMESITE = "Lax"
JWT_SECRET = FI_JWT_SECRET
JWT_SECRET_API = FI_JWT_SECRET_API

# Session
SESSION_COOKIE_AGE = 40 * 60
MOBILE_SESSION_AGE = 30 * 24 * 60 * 60

# Analytics
MIXPANEL_API_TOKEN = FI_MIXPANEL_API_TOKEN

# Cache
CACHE_TTL = 60 * 60 * 8

# Static files
STATIC_BUCKET_NAME = 'fluidintegrates-static'
AWS_STORAGE_BUCKET_NAME = f'{STATIC_BUCKET_NAME}-{CI_COMMIT_REF_NAME}'
AWS_S3_CUSTOM_DOMAIN = 'd1l3f50ot7vyg9.cloudfront.net'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/integrates/static/dashboard'
