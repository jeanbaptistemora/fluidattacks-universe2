import os
from typing import (
    Optional,
)

try:
    CI_COMMIT_REF_NAME = os.environ["CI_COMMIT_REF_NAME"]
    CI_COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
    CI_COMMIT_SHORT_SHA = CI_COMMIT_SHA[0:8]
    FI_AWS_DYNAMODB_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_DYNAMODB_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_BATCH_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_BATCH_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_CLOUDWATCH_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_CLOUDWATCH_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_S3_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_S3_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_SECRETSMANAGER_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_SECRETSMANAGER_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
    FI_AZUREAD_OAUTH2_KEY = os.environ["AZUREAD_OAUTH2_KEY"]
    FI_AZUREAD_OAUTH2_SECRET = os.environ["AZUREAD_OAUTH2_SECRET"]
    FI_BITBUCKET_OAUTH2_KEY = os.environ["BITBUCKET_OAUTH2_KEY"]
    FI_BITBUCKET_OAUTH2_SECRET = os.environ["BITBUCKET_OAUTH2_SECRET"]
    FI_BUGSNAG_ACCESS_TOKEN = os.environ["BUGSNAG_ACCESS_TOKEN"]
    FI_BUGSNAG_API_KEY_SCHEDULER = os.environ["BUGSNAG_API_KEY_SCHEDULER"]
    FI_CHARTS_LOGO_PATH = os.environ["INTEGRATES_CHARTS_LOGO_PATH"]
    FI_CLOUDMERSIVE_API_KEY = os.environ["CLOUDMERSIVE_API_KEY"]
    FI_COMMUNITY_PROJECTS = os.environ["COMMUNITY_PROJECTS"]
    FI_DB_MODEL_PATH = os.environ["INTEGRATES_DB_MODEL_PATH"]
    FI_DEBUG = os.environ["DEBUG"]
    FI_DEFAULT_ORG = os.environ["DEFAULT_ORG"]
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
    FI_MAIL_PRODUCTION = os.environ["MAIL_PRODUCTION"]
    FI_MAIL_PROJECTS = os.environ["MAIL_PROJECTS"]
    FI_MAIL_REVIEWERS = os.environ["MAIL_REVIEWERS"]
    FI_MANDRILL_API_KEY = os.environ["MANDRILL_APIKEY"]
    FI_MIXPANEL_API_TOKEN = os.environ["MIXPANEL_API_TOKEN"]
    FI_NEW_RELIC_API_KEY = os.environ["NEW_RELIC_API_KEY"]
    FI_NEW_RELIC_APP_ID = os.environ["NEW_RELIC_APP_ID"]
    FI_NEW_RELIC_ENVIRONMENT = os.environ["NEW_RELIC_ENVIRONMENT"]
    FI_NEW_RELIC_LICENSE_KEY = os.environ["NEW_RELIC_LICENSE_KEY"]
    FI_REDIS_SERVER = os.environ["REDIS_SERVER"]
    FI_STARLETTE_SESSION_KEY = os.environ["STARLETTE_SESSION_KEY"]
    FI_TEST_PROJECTS = os.environ["TEST_PROJECTS"]
    FI_ZENDESK_EMAIL = os.environ["ZENDESK_EMAIL"]
    FI_ZENDESK_SUBDOMAIN = os.environ["ZENDESK_SUBDOMAIN"]
    FI_ZENDESK_TOKEN = os.environ["ZENDESK_TOKEN"]
    LOG_LEVEL_CONSOLE: Optional[str] = os.environ.get("LOG_LEVEL_CONSOLE")
    LOG_LEVEL_BUGSNAG: Optional[str] = os.environ.get("LOG_LEVEL_BUGSNAG")
    LOG_LEVEL_WATCHTOWER: Optional[str] = os.environ.get(
        "LOG_LEVEL_WATCHTOWER"
    )
    PRODUCT_API_TOKEN: Optional[str] = os.environ.get("PRODUCT_API_TOKEN")
    SERVICES_GITLAB_API_TOKEN = os.environ["SERVICES_GITLAB_API_TOKEN"]
    SERVICES_GITLAB_API_USER = os.environ["SERVICES_GITLAB_API_USER"]
    SERVICES_PROD_AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get(
        "SERVICES_PROD_AWS_ACCESS_KEY_ID", ""
    )
    SERVICES_PROD_AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get(
        "SERVICES_PROD_AWS_SECRET_ACCESS_KEY", ""
    )
    SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]
    STARTDIR = os.environ["STARTDIR"]

    # not secrets but must be environment vars
    BASE_URL = "https://app.fluidattacks.com"
    FI_AWS_REDSHIFT_PORT = 5439
    FI_AWS_S3_ANALYTICS_BUCKET = "fluidintegrates.analytics"
    FI_AWS_S3_BUCKET = "fluidintegrates.evidences"
    FI_AWS_S3_FORCES_BUCKET = "fluidintegrates.forces"
    FI_AWS_S3_REPORTS_BUCKET = "fluidintegrates.reports"
    FI_AWS_S3_RESOURCES_BUCKET = "fluidintegrates.resources"
    FI_NEW_RELIC_CONF_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "newrelic.ini"
    )
    SERVICES_AWS_S3_DATA_BUCKET = "continuous-data"
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise
