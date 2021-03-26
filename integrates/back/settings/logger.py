# Settings logger-related configs

import os
import json
import logging.config
from logging import LogRecord
from typing import Any
from boto3.session import Session
import bugsnag
import requests
from graphql import GraphQLError
from backend.exceptions import (
    DocumentNotFound,
    UnavailabilityError,
)

from back import settings

from __init__ import (
    CI_COMMIT_SHA,
    CI_COMMIT_SHORT_SHA,
    FI_AWS_CLOUDWATCH_ACCESS_KEY,
    FI_AWS_CLOUDWATCH_SECRET_KEY,
    FI_BUGSNAG_ACCESS_TOKEN,
    FI_ENVIRONMENT
)


# logging
AWS_ACCESS_KEY_ID = FI_AWS_CLOUDWATCH_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = FI_AWS_CLOUDWATCH_SECRET_KEY  # noqa
AWS_REGION_NAME = 'us-east-1'

BOTO3_SESSION = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
    region_name=AWS_REGION_NAME
)


# pylint: disable=too-few-public-methods
class RequireDebugFalse(logging.Filter):

    def filter(self, _: LogRecord) -> bool:
        return not settings.DEBUG


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': RequireDebugFalse
        },
    },
    'formatters': {
        'level_message_extra': {
            'format': '[{levelname}] {message}, extra={extra}',
            'style': '{',
        },
    },
    'handlers': {
        'bugsnag': {
            'extra_fields': {'extra': ['extra']},
            'class': 'bugsnag.handlers.BugsnagHandler',
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'level_message_extra',
        },
        'watchtower': {
            'boto3_session': BOTO3_SESSION,
            'class': 'watchtower.CloudWatchLogHandler',
            'level': 'INFO',
            'log_group': 'FLUID',
            'filters': ['require_debug_false'],
            'stream_name': 'FLUIDIntegrates',

            # Since LogGroup already exists, it was causing a
            # ThrottlingException error that resulted in 'unable to configure
            # watchtower'
            'create_log_group': False,
        },
    },
    'loggers': {
        'app': {
            'handlers': ['bugsnag', 'console'],
            'level': 'INFO'
        },
        'backend': {
            'handlers': ['bugsnag', 'console'],
            'level': 'INFO'
        },
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'schedulers': {
            'handlers': ['bugsnag', 'console'],
            'level': 'INFO'
        },
        'transactional': {
            'handlers': ['console', 'watchtower'],
            'level': 'INFO'
        }
    }
}

NOEXTRA = {'extra': {'extra': None}}

# Force logging to load the config right away
# This is important otherwise loggers are not going to work in CI jobs
logging.config.dictConfig(LOGGING)


# bugsnag
bugsnag.configure(
    api_key=FI_BUGSNAG_ACCESS_TOKEN,
    app_version=CI_COMMIT_SHORT_SHA,
    asynchronous=True,
    auto_capture_sessions=True,
    project_root=settings.BASE_DIR,
    release_stage=FI_ENVIRONMENT,
    send_environment=True
)

if FI_ENVIRONMENT == 'production':
    URL = 'https://build.bugsnag.com'
    HEADERS = {'Content-Type': 'application/json', 'server': 'None'}
    PAYLOAD = {
        'apiKey': FI_BUGSNAG_ACCESS_TOKEN,
        'appVersion': CI_COMMIT_SHORT_SHA,
        'releaseStage': FI_ENVIRONMENT,
        'sourceControl': {
            'provider': 'gitlab',
            'repository': 'https://gitlab.com/fluidattacks/product.git',
            'revision': f'{CI_COMMIT_SHA}/integrates/back/packages',
        },
    }
    requests.post(URL, headers=HEADERS, data=json.dumps(PAYLOAD))


def customize_bugsnag_error_reports(notification: Any) -> None:
    """Handle for expected errors and customization"""
    ex_msg = str(notification.exception)

    notification.grouping_hash = ex_msg

    # Customize Login required error
    if isinstance(notification.exception, UnavailabilityError):
        notification.unhandled = False
    if isinstance(notification.exception, GraphQLError) and \
            ex_msg == 'Login required':
        notification.severity = 'warning'
        notification.unhandled = False
    if isinstance(notification.exception, DocumentNotFound):
        notification.severity = 'info'


bugsnag.before_notify(customize_bugsnag_error_reports)
