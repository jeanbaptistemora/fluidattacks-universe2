import os

try:
    FI_AWS_DYNAMODB_ACCESS_KEY = os.environ['FI_AWS_DYNAMODB_ACCESS_KEY']
    FI_AWS_DYNAMODB_SECRET_KEY = os.environ['FI_AWS_DYNAMODB_SECRET_KEY']
    FI_CLOUDFRONT_ACCESS_KEY = os.environ['FI_CLOUDFRONT_ACCESS_KEY']
    FI_CLOUDFRONT_PRIVATE_KEY = os.environ['FI_CLOUDFRONT_PRIVATE_KEY']
    FI_CLOUDFRONT_RESOURCES_DOMAIN = os.environ['FI_CLOUDFRONT_RESOURCES_DOMAIN']
    FI_DJANGO_SECRET_KEY = os.environ['FI_DJANGO_SECRET_KEY']
    FI_DB_USER = os.environ['FI_DB_USER']
    FI_DB_PASSWD = os.environ['FI_DB_PASSWD']
    FI_DB_HOST = os.environ['FI_DB_HOST']
    FI_AWS_CLOUDWATCH_ACCESS_KEY = os.environ['FI_AWS_CLOUDWATCH_ACCESS_KEY']
    FI_AWS_CLOUDWATCH_SECRET_KEY = os.environ['FI_AWS_CLOUDWATCH_SECRET_KEY']
    FI_MIXPANEL_API_TOKEN = os.environ['FI_MIXPANEL_API_TOKEN']
    FI_INTERCOM_APPID = os.environ['FI_INTERCOM_APPID']
    FI_INTERCOM_SECURE_KEY = os.environ['FI_INTERCOM_SECURE_KEY']
    FI_SLACK_BOT_ID = os.environ['FI_SLACK_BOT_ID']
    FI_SLACK_BOT_TOKEN = os.environ['FI_SLACK_BOT_TOKEN']
    FI_GOOGLE_OAUTH2_KEY = os.environ['FI_GOOGLE_OAUTH2_KEY']
    FI_GOOGLE_OAUTH2_SECRET = os.environ['FI_GOOGLE_OAUTH2_SECRET']
    FI_AZUREAD_OAUTH2_KEY = os.environ['FI_AZUREAD_OAUTH2_KEY']
    FI_AZUREAD_OAUTH2_SECRET = os.environ['FI_AZUREAD_OAUTH2_SECRET']
    FI_DRIVE_AUTHORIZATION = os.environ['FI_DRIVE_AUTHORIZATION']
    FI_FORMSTACK_TOKENS = os.environ['FI_FORMSTACK_TOKENS']
    FI_AWS_OUTPUT = os.environ['FI_AWS_OUTPUT']
    FI_DEBUG = os.environ['FI_DEBUG']
    FI_ROLLBAR_ACCESS_TOKEN = os.environ['FI_ROLLBAR_ACCESS_TOKEN']
    FI_AWS_S3_ACCESS_KEY = os.environ['FI_AWS_S3_ACCESS_KEY']
    FI_AWS_S3_SECRET_KEY = os.environ['FI_AWS_S3_SECRET_KEY']
    FI_AWS_S3_BUCKET = os.environ['FI_AWS_S3_BUCKET']
    FI_AWS_S3_RESOURCES_BUCKET = os.environ['FI_AWS_S3_RESOURCES_BUCKET']
    FI_ENVIRONMENT = os.environ['FI_ENVIRONMENT']
    FI_MANDRILL_API_KEY = os.environ['FI_MANDRILL_API_KEY']
    FI_JWT_SECRET = os.environ['FI_JWT_SECRET']
    FI_JWT_SECRET_API = os.environ['FI_JWT_SECRET_API']
    FI_REDIS_SERVER = os.environ['FI_REDIS_SERVER']
    FI_MAIL_CONTINUOUS = os.environ['FI_MAIL_CONTINUOUS']
    FI_MAIL_ENGINEERING = os.environ['FI_MAIL_ENGINEERING']
    FI_MAIL_PROJECTS = os.environ['FI_MAIL_PROJECTS']
    FI_MAIL_REVIEWERS = os.environ['FI_MAIL_REVIEWERS']
    FI_MAIL_REPLYERS = os.environ['FI_MAIL_REPLYERS']
    FI_TEST_PROJECTS = os.environ['FI_TEST_PROJECTS']
    FI_AWS_REDSHIFT_DB_NAME = os.environ['FI_AWS_REDSHIFT_DB_NAME']
    FI_AWS_REDSHIFT_USER = os.environ['FI_AWS_REDSHIFT_USER']
    FI_AWS_REDSHIFT_PASSWORD = os.environ['FI_AWS_REDSHIFT_PASSWORD']
    FI_AWS_REDSHIFT_HOST = os.environ['FI_AWS_REDSHIFT_HOST']
    FI_AWS_REDSHIFT_PORT = os.environ['FI_AWS_REDSHIFT_PORT']
    FI_GOOGLE_OAUTH2_KEY_ANDROID = os.environ['FI_GOOGLE_OAUTH2_KEY_ANDROID']
    FI_GOOGLE_OAUTH2_KEY_IOS = os.environ['FI_GOOGLE_OAUTH2_KEY_IOS']
except KeyError as e:
    print("Environment variable " + e.args[0] + " doesn't exist")
    raise
