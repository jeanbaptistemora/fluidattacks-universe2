import os
from typing import (
    Optional,
)

try:
    CI_COMMIT_REF_NAME = os.environ["CI_COMMIT_REF_NAME"]
    CI_COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
    CI_COMMIT_SHORT_SHA = CI_COMMIT_SHA[0:8]
    FI_AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_OPENSEARCH_HOST = os.environ["AWS_OPENSEARCH_HOST"]
    FI_AWS_REDSHIFT_DBNAME = os.environ.get("AWS_REDSHIFT_DBNAME")
    FI_AWS_REDSHIFT_HOST = os.environ.get("AWS_REDSHIFT_HOST")
    FI_AWS_REDSHIFT_PASSWORD = os.environ.get("AWS_REDSHIFT_PASSWORD")
    FI_AWS_REDSHIFT_USER = os.environ.get("AWS_REDSHIFT_USER")
    FI_AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
    FI_AZUREAD_OAUTH2_KEY = os.environ["AZUREAD_OAUTH2_KEY"]
    FI_AZUREAD_OAUTH2_SECRET = os.environ["AZUREAD_OAUTH2_SECRET"]
    FI_BITBUCKET_OAUTH2_KEY = os.environ["BITBUCKET_OAUTH2_KEY"]
    FI_BITBUCKET_OAUTH2_SECRET = os.environ["BITBUCKET_OAUTH2_SECRET"]
    FI_BUGSNAG_ACCESS_TOKEN = os.environ["BUGSNAG_ACCESS_TOKEN"]
    FI_BUGSNAG_API_KEY_SCHEDULER = os.environ["BUGSNAG_API_KEY_SCHEDULER"]
    FI_CHARTS_LOGO_PATH = os.environ["INTEGRATES_CHARTS_LOGO_PATH"]
    FI_DB_MODEL_PATH = os.environ["INTEGRATES_DB_MODEL_PATH"]
    FI_DEBUG = os.environ["DEBUG"]
    FI_DYNAMODB_HOST = os.environ["DYNAMODB_HOST"]
    FI_DYNAMODB_PORT = os.environ["DYNAMODB_PORT"]
    FI_EMAIL_TEMPLATES: str = os.environ["INTEGRATES_MAILER_TEMPLATES"]
    FI_ENVIRONMENT = os.environ["ENVIRONMENT"]
    FI_GOOGLE_OAUTH2_KEY = os.environ["GOOGLE_OAUTH2_KEY"]
    FI_GOOGLE_OAUTH2_SECRET = os.environ["GOOGLE_OAUTH2_SECRET"]
    FI_JWT_ENCRYPTION_KEY = os.environ["JWT_ENCRYPTION_KEY"]
    FI_JWT_SECRET = os.environ["JWT_SECRET"]
    FI_JWT_SECRET_API = os.environ["JWT_SECRET_API"]
    FI_MAIL_CONTINUOUS = os.environ["MAIL_CONTINUOUS"]
    FI_MAIL_COS = os.environ["MAIL_COS"]
    FI_MAIL_CTO = os.environ["MAIL_CTO"]
    FI_MAIL_CUSTOMER_SUCCESS = os.environ["MAIL_CUSTOMER_SUCCESS"]
    FI_MAIL_PRODUCTION = os.environ["MAIL_PRODUCTION"]
    FI_MAIL_PROJECTS = os.environ["MAIL_PROJECTS"]
    FI_MAIL_REVIEWERS = os.environ["MAIL_REVIEWERS"]
    FI_MANDRILL_API_KEY = os.environ["MANDRILL_APIKEY"]
    FI_MIXPANEL_API_TOKEN = os.environ["MIXPANEL_API_TOKEN"]
    FI_REDIS_SERVER = os.environ["REDIS_SERVER"]
    FI_STARLETTE_SESSION_KEY = os.environ["STARLETTE_SESSION_KEY"]
    FI_STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
    FI_STRIPE_WEBHOOK_KEY = os.environ["STRIPE_WEBHOOK_KEY"]
    FI_TEST_PROJECTS = os.environ["TEST_PROJECTS"]
    FI_TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    FI_TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    FI_TWILIO_VERIFY_SERVICE_SID = os.environ["TWILIO_VERIFY_SERVICE_SID"]
    FI_ZENDESK_EMAIL = os.environ["ZENDESK_EMAIL"]
    FI_ZENDESK_SUBDOMAIN = os.environ["ZENDESK_SUBDOMAIN"]
    FI_ZENDESK_TOKEN = os.environ["ZENDESK_TOKEN"]
    LOG_LEVEL_CONSOLE: Optional[str] = os.environ.get("LOG_LEVEL_CONSOLE")
    LOG_LEVEL_BUGSNAG: Optional[str] = os.environ.get("LOG_LEVEL_BUGSNAG")
    LOG_LEVEL_WATCHTOWER: Optional[str] = os.environ.get(
        "LOG_LEVEL_WATCHTOWER"
    )
    UNIVERSE_API_TOKEN: Optional[str] = os.environ.get("UNIVERSE_API_TOKEN")
    SERVICES_GITLAB_API_TOKEN = os.environ["SERVICES_GITLAB_API_TOKEN"]
    SERVICES_GITLAB_API_USER = os.environ["SERVICES_GITLAB_API_USER"]
    STARTDIR = os.environ["STARTDIR"]

    # not secrets but must be environment vars
    BASE_URL = "https://app.fluidattacks.com"
    FI_AWS_REDSHIFT_PORT = 5439
    FI_AWS_REGION_NAME = "us-east-1"
    FI_AWS_S3_ANALYTICS_BUCKET = "fluidintegrates.analytics"
    FI_AWS_S3_BUCKET = "fluidintegrates.evidences"
    FI_AWS_S3_FORCES_BUCKET = "fluidintegrates.forces"
    FI_AWS_S3_MIRRORS_BUCKET = "continuous-repositories"
    FI_AWS_S3_REPORTS_BUCKET = "fluidintegrates.reports"
    FI_AWS_S3_RESOURCES_BUCKET = "fluidintegrates.resources"
    SERVICES_AWS_S3_DATA_BUCKET = "continuous-data"
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise
