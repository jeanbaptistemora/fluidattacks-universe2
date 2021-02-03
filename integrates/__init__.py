import os

try:
    CI_COMMIT_AUTHOR = os.environ['CI_COMMIT_AUTHOR']
    CI_COMMIT_REF_NAME = os.environ['CI_COMMIT_REF_NAME']
    CI_COMMIT_SHA = os.environ['CI_COMMIT_SHA']
    CI_COMMIT_SHORT_SHA = os.environ['CI_COMMIT_SHORT_SHA']
    CI_PROJECT_ID = os.environ['CI_PROJECT_ID']
    FI_AWS_DYNAMODB_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_DYNAMODB_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_BITBUCKET_OAUTH2_KEY = os.environ['BITBUCKET_OAUTH2_KEY']
    FI_BITBUCKET_OAUTH2_SECRET = os.environ['BITBUCKET_OAUTH2_SECRET']
    FI_BUGSNAG_ACCESS_TOKEN = os.environ['BUGSNAG_ACCESS_TOKEN']
    FI_BUGSNAG_API_KEY_SCHEDULER = os.environ['BUGSNAG_API_KEY_SCHEDULER']
    FI_COMMUNITY_PROJECTS = os.environ['COMMUNITY_PROJECTS']
    FI_DYNAMODB_HOST = os.environ['DYNAMODB_HOST']
    FI_DYNAMODB_PORT = os.environ['DYNAMODB_PORT']
    FI_CLOUDFRONT_ACCESS_KEY = os.environ['CLOUDFRONT_ACCESS_KEY']
    FI_CLOUDFRONT_PRIVATE_KEY = os.environ['CLOUDFRONT_PRIVATE_KEY']
    FI_CLOUDFRONT_RESOURCES_DOMAIN = os.environ['CLOUDFRONT_RESOURCES_DOMAIN']
    FI_CLOUDFRONT_REPORTS_DOMAIN = os.environ['CLOUDFRONT_REPORTS_DOMAIN']
    FI_CLOUDMERSIVE_API_KEY = os.environ['CLOUDMERSIVE_API_KEY']
    FI_AWS_CLOUDWATCH_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_CLOUDWATCH_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_MIXPANEL_API_TOKEN = os.environ['MIXPANEL_API_TOKEN']
    FI_GOOGLE_OAUTH2_KEY = os.environ['GOOGLE_OAUTH2_KEY']
    FI_GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_OAUTH2_SECRET']
    FI_AZUREAD_OAUTH2_KEY = os.environ['AZUREAD_OAUTH2_KEY']
    FI_AZUREAD_OAUTH2_SECRET = os.environ['AZUREAD_OAUTH2_SECRET']
    FI_DEBUG = os.environ['DEBUG']
    FI_AWS_S3_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    FI_AWS_S3_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    FI_ENVIRONMENT = os.environ['ENVIRONMENT']
    FI_DEFAULT_ORG = os.environ['DEFAULT_ORG']
    FI_MANDRILL_API_KEY = os.environ['MANDRILL_APIKEY']
    FI_JWT_ENCRYPTION_KEY = os.environ['JWT_ENCRYPTION_KEY']
    FI_JWT_SECRET = os.environ['JWT_SECRET']
    FI_JWT_SECRET_API = os.environ['JWT_SECRET_API']
    FI_REDIS_SERVER = os.environ['REDIS_SERVER']
    FI_MAIL_CONTINUOUS = os.environ['MAIL_CONTINUOUS']
    FI_MAIL_PRODUCTION = os.environ['MAIL_PRODUCTION']
    FI_MAIL_PROJECTS = os.environ['MAIL_PROJECTS']
    FI_MAIL_REVIEWERS = os.environ['MAIL_REVIEWERS']
    FI_MAIL_RESOURCERS = os.environ['MAIL_RESOURCERS']
    FI_TEST_PROJECTS = os.environ['TEST_PROJECTS']
    FI_STARLETTE_SESSION_KEY = os.environ['STARLETTE_SESSION_KEY']
    FI_ZENDESK_EMAIL = os.environ['ZENDESK_EMAIL']
    FI_ZENDESK_SUBDOMAIN = os.environ['ZENDESK_SUBDOMAIN']
    FI_ZENDESK_TOKEN = os.environ['ZENDESK_TOKEN']
    SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']

    # not secrets but must be environment vars
    BASE_URL = 'https://integrates.fluidattacks.com'
    FI_AWS_REDSHIFT_PORT = 5439
    FI_AWS_S3_BUCKET = 'fluidintegrates.evidences'
    FI_AWS_S3_ANALYTICS_BUCKET = 'fluidintegrates.analytics'
    FI_AWS_S3_RESOURCES_BUCKET = 'fluidintegrates.resources'
    FI_AWS_S3_REPORTS_BUCKET = 'fluidintegrates.reports'
    FI_AWS_S3_FORCES_BUCKET = 'fluidintegrates.forces'
    SERVICES_AWS_S3_DATA_BUCKET = 'continuous-data'
except KeyError as e:
    print("Environment variable " + e.args[0] + " doesn't exist")
    raise
