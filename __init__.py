import os

try:
    FI_AWS_DYNAMODB_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_DYNAMODB_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_DYNAMODB_HOST = os.environ['DYNAMODB_HOST']
    FI_DYNAMODB_PORT = os.environ['DYNAMODB_PORT']
    FI_CLOUDFRONT_ACCESS_KEY = os.environ['CLOUDFRONT_ACCESS_KEY']
    FI_CLOUDFRONT_PRIVATE_KEY = os.environ['CLOUDFRONT_PRIVATE_KEY']
    FI_CLOUDFRONT_RESOURCES_DOMAIN = os.environ['CLOUDFRONT_RESOURCES_DOMAIN']
    FI_DJANGO_SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    FI_DB_USER = os.environ['DB_USER']
    FI_DB_PASSWD = os.environ['DB_PASSWD']
    FI_DB_HOST = os.environ['DB_HOST']
    FI_AWS_CLOUDWATCH_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_CLOUDWATCH_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_MIXPANEL_API_TOKEN = os.environ['MIXPANEL_API_TOKEN']
    FI_INTERCOM_APPID = os.environ['INTERCOM_API_ID']
    FI_INTERCOM_SECURE_KEY = os.environ['INTERCOM_SECURE_KEY']
    FI_SLACK_BOT_ID = os.environ['SLACK_BOT_ID']
    FI_SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    FI_GOOGLE_OAUTH2_KEY = os.environ['GOOGLE_OAUTH2_KEY']
    FI_GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_OAUTH2_SECRET']
    FI_AZUREAD_OAUTH2_KEY = os.environ['AZUREAD_OAUTH2_KEY']
    FI_AZUREAD_OAUTH2_SECRET = os.environ['AZUREAD_OAUTH2_SECRET']
    FI_DEBUG = os.environ['DEBUG']
    FI_ROLLBAR_ACCESS_TOKEN = os.environ['ROLLBAR_ACCESS_TOKEN']
    FI_AWS_S3_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_S3_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_ENVIRONMENT = os.environ['ENVIRONMENT']
    FI_MANDRILL_API_KEY = os.environ['MANDRILL_APIKEY']
    FI_JWT_SECRET = os.environ['JWT_SECRET']
    FI_JWT_SECRET_API = os.environ['JWT_SECRET_API']
    FI_REDIS_SERVER = os.environ['REDIS_SERVER']
    FI_MAIL_CONTINUOUS = os.environ['MAIL_CONTINUOUS']
    FI_MAIL_PRODUCTION = os.environ['MAIL_PRODUCTION']
    FI_MAIL_PROJECTS = os.environ['MAIL_PROJECTS']
    FI_MAIL_REVIEWERS = os.environ['MAIL_REVIEWERS']
    FI_MAIL_REPLYERS = os.environ['MAIL_REPLYERS']
    FI_TEST_PROJECTS = os.environ['TEST_PROJECTS']
    FI_AWS_REDSHIFT_DB_NAME = os.environ['AWS_REDSHIFT_DBNAME']
    FI_AWS_REDSHIFT_USER = os.environ['AWS_REDSHIFT_USER']
    FI_AWS_REDSHIFT_PASSWORD = os.environ['AWS_REDSHIFT_PASSWORD']
    FI_AWS_REDSHIFT_HOST = os.environ['AWS_REDSHIFT_HOST']
    FI_GOOGLE_OAUTH2_KEY_ANDROID = os.environ['GOOGLE_OAUTH2_KEY_ANDROID']
    FI_GOOGLE_OAUTH2_KEY_IOS = os.environ['GOOGLE_OAUTH2_KEY_IOS']
    SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
    BREAK_BUILD_TRIGGER_URL = os.environ['BREAK_BUILD_TRIGGER_URL']
    BREAK_BUILD_TRIGGER_REF = os.environ['BREAK_BUILD_TRIGGER_REF']
    BREAK_BUILD_TRIGGER_TOKEN = os.environ['BREAK_BUILD_TRIGGER_TOKEN']

    # not secrets but must be environ vars
    FI_AWS_REDSHIFT_PORT = 5439
    FI_AWS_S3_BUCKET = 'fluidintegrates.evidences'
    FI_AWS_S3_RESOURCES_BUCKET = 'fluidintegrates.resources'
except KeyError as e:
    print("Environment variable " + e.args[0] + " doesn't exist")
    raise
